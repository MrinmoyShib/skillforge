"""
Aggregates user stats, category mastery, recent submissions, and recommendations for the Dashboard.
"""
from django.db.models import Sum
from apps.problems.models import Category, Problem
from apps.submissions.models import Submission
from apps.progress.models import UserProgress
from apps.progress.selectors.progress_selectors import (
    get_user_progress_summary,
    get_user_activity_feed,
)


def get_aggregated_dashboard_data(user) -> dict:
    """
    Builds the unified dashboard response for the authenticated user.
    """
    stats = get_user_progress_summary(user)

    # 1. Category Mastery Calculation
    categories = Category.objects.all().order_by('display_order', 'id')
    category_mastery = []

    solved_problem_ids = list(
        UserProgress.objects.filter(user=user, solved=True).values_list('problem_id', flat=True)
    )

    for cat in categories:
        cat_problems = Problem.objects.filter(category=cat, is_published=True)
        total = cat_problems.count()
        solved_count = UserProgress.objects.filter(
            user=user,
            problem__category=cat,
            problem__is_published=True,
            solved=True
        ).count()
        percent = round((solved_count / total) * 100, 1) if total > 0 else 0.0

        beginner_total = cat_problems.filter(challenge_level__in=[1, 2]).count()
        beginner_solved = UserProgress.objects.filter(
            user=user,
            problem__category=cat,
            problem__challenge_level__in=[1, 2],
            problem__is_published=True,
            solved=True
        ).count()

        intermediate_total = cat_problems.filter(challenge_level__in=[3, 4]).count()
        intermediate_solved = UserProgress.objects.filter(
            user=user,
            problem__category=cat,
            problem__challenge_level__in=[3, 4],
            problem__is_published=True,
            solved=True
        ).count()

        master_total = cat_problems.filter(challenge_level=5).count()
        master_solved = UserProgress.objects.filter(
            user=user,
            problem__category=cat,
            problem__challenge_level=5,
            problem__is_published=True,
            solved=True
        ).count()

        xp_earned = UserProgress.objects.filter(
            user=user,
            problem__category=cat,
            problem__is_published=True,
            solved=True
        ).aggregate(total=Sum('xp_awarded'))['total'] or 0

        total_xp = cat_problems.aggregate(total=Sum('xp_reward'))['total'] or 0
        remaining_problems = max(0, total - solved_count)

        next_unsolved = cat_problems.exclude(id__in=solved_problem_ids).order_by('challenge_level', 'id').first()

        category_mastery.append({
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,
            "total_problems": total,
            "solved_problems": solved_count,
            "remaining_problems": remaining_problems,
            "xp_earned": xp_earned,
            "total_xp": total_xp,
            "mastery_percent": percent,
            "beginner_total": beginner_total,
            "beginner_solved": beginner_solved,
            "intermediate_total": intermediate_total,
            "intermediate_solved": intermediate_solved,
            "master_total": master_total,
            "master_solved": master_solved,
            "next_unsolved_slug": next_unsolved.slug if next_unsolved else None,
        })

    # 2. Recent Submissions
    submissions_qs = (
        Submission.objects.filter(user=user)
        .select_related('problem')
        .order_by('-created_at')[:5]
    )
    recent_submissions = [
        {
            "id": sub.id,
            "problem_id": sub.problem.id,
            "problem_title": sub.problem.title,
            "problem_slug": sub.problem.slug,
            "language": getattr(sub, 'language', 'cpp'),
            "difficulty": sub.problem.difficulty,
            "status": sub.status,
            "execution_time": sub.execution_time,
            "memory_usage": sub.memory_usage,
            "passed_cases": sub.passed_test_cases_count,
            "total_cases": sub.total_test_cases_count,
            "is_sample_run": sub.is_sample_run,
            "created_at": sub.created_at,
        }
        for sub in submissions_qs
    ]

    # 3. Recommended Next Challenges (Personalized per language track)
    recommended_problems = []
    for cat in categories:
        unsolved_in_cat = (
            Problem.objects.filter(category=cat, is_published=True)
            .exclude(id__in=solved_problem_ids)
            .order_by('challenge_level', 'id')
            .first()
        )
        if unsolved_in_cat:
            recommended_problems.append({
                "id": unsolved_in_cat.id,
                "title": unsolved_in_cat.title,
                "slug": unsolved_in_cat.slug,
                "category_name": unsolved_in_cat.category.name if unsolved_in_cat.category else "Track",
                "language": getattr(unsolved_in_cat, 'language', cat.slug),
                "difficulty": unsolved_in_cat.difficulty,
                "challenge_level": unsolved_in_cat.challenge_level,
                "xp_reward": unsolved_in_cat.xp_reward,
            })

    if len(recommended_problems) < 3:
        existing_ids = [p["id"] for p in recommended_problems]
        extra_unsolved = (
            Problem.objects.filter(is_published=True)
            .exclude(id__in=solved_problem_ids + existing_ids)
            .select_related('category')
            .order_by('challenge_level', 'id')[:(3 - len(recommended_problems))]
        )
        for p in extra_unsolved:
            recommended_problems.append({
                "id": p.id,
                "title": p.title,
                "slug": p.slug,
                "category_name": p.category.name if p.category else "Track",
                "language": getattr(p, 'language', 'cpp'),
                "difficulty": p.difficulty,
                "challenge_level": p.challenge_level,
                "xp_reward": p.xp_reward,
            })

    # 4. Recent Activity Log
    activity_qs = get_user_activity_feed(user, limit=5)
    recent_activity = [
        {
            "id": act.id,
            "activity_type": act.activity_type,
            "description": act.description,
            "metadata": act.metadata,
            "created_at": act.created_at,
        }
        for act in activity_qs
    ]

    # 5. Enrolled & Completed Guided Engineering Projects
    from apps.projects.models import UserProjectProgress
    enrolled_projects_qs = (
        UserProjectProgress.objects.filter(user=user)
        .select_related('project')
        .prefetch_related('project__milestones')
        .order_by('-updated_at')
    )
    enrolled_projects = []
    for up in enrolled_projects_qs:
        total_m = up.project.milestones.count()
        completed_m = len(up.completed_milestones or [])
        progress_pct = round((completed_m / total_m) * 100, 1) if total_m > 0 else 0.0
        enrolled_projects.append({
            "id": up.project.id,
            "title": up.project.title,
            "slug": up.project.slug,
            "language": up.project.language,
            "difficulty": up.project.difficulty,
            "status": up.status,
            "current_milestone_order": up.current_milestone_order,
            "completed_milestones_count": completed_m,
            "total_milestones_count": total_m,
            "progress_percent": progress_pct,
            "xp_reward": up.project.xp_reward,
            "started_at": up.started_at,
            "completed_at": up.completed_at,
        })

    return {
        "stats": stats,
        "category_mastery": category_mastery,
        "recent_submissions": recent_submissions,
        "recommended_problems": recommended_problems,
        "recent_activity": recent_activity,
        "enrolled_projects": enrolled_projects,
    }

