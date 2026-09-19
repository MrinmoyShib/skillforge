"""
Aggregation selector for public developer portfolio showcase.
"""
from typing import Optional, Dict, Any
from django.db.models import Count, Sum
from apps.accounts.models import User
from apps.problems.models import Category, Problem, Tag
from apps.progress.models import UserProgress, ActivityLog
from apps.progress.services.leveling import calculate_level
from apps.achievements.models import UserAchievement
from apps.projects.models import UserProjectProgress


def get_public_portfolio(username: str) -> Optional[Dict[str, Any]]:
    """
    Builds the public portfolio payload for the given username.
    Returns None if user does not exist.
    """
    user = User.objects.filter(username=username).select_related('profile').first()
    if not user:
        return None

    profile = user.profile

    # 1. Track Mastery Breakdown
    track_categories = Category.objects.filter(slug__in=['python', 'javascript', 'cpp']).order_by('display_order')
    tracks_data = []

    for cat in track_categories:
        total_p = Problem.objects.filter(category=cat, is_published=True).count()
        solved_count = UserProgress.objects.filter(
            user=user,
            problem__category=cat,
            problem__is_published=True,
            solved=True
        ).count()
        xp_earned = UserProgress.objects.filter(
            user=user,
            problem__category=cat,
            problem__is_published=True,
            solved=True
        ).aggregate(total=Sum('xp_awarded'))['total'] or 0

        percent = round((solved_count / total_p) * 100, 1) if total_p > 0 else 0.0

        tracks_data.append({
            "slug": cat.slug,
            "name": cat.name,
            "total_problems": total_p,
            "solved_problems": solved_count,
            "xp_earned": xp_earned,
            "mastery_percent": percent,
        })

    # 2. Verified Completed Guided Projects
    completed_projects_qs = (
        UserProjectProgress.objects.filter(user=user, status='COMPLETED')
        .select_related('project')
        .order_by('-completed_at')
    )
    verified_projects = [
        {
            "id": up.project.id,
            "title": up.project.title,
            "slug": up.project.slug,
            "language": up.project.language,
            "difficulty": up.project.difficulty,
            "short_description": up.project.short_description,
            "technologies": up.project.technologies or [],
            "xp_reward": up.project.xp_reward,
            "completed_at": up.completed_at,
        }
        for up in completed_projects_qs
    ]

    # 3. Algorithmic Domain Mastery (by Tag)
    solved_progress = UserProgress.objects.filter(user=user, solved=True).select_related('problem')
    tag_counts = (
        Tag.objects.filter(problems__progress_records__in=solved_progress)
        .annotate(solved_count=Count('problems'))
        .order_by('-solved_count')[:10]
    )
    skill_domains = [
        {
            "slug": t.slug,
            "name": t.name,
            "solved_count": t.solved_count,
        }
        for t in tag_counts
    ]

    # 4. Unlocked Achievements
    user_achievements = (
        UserAchievement.objects.filter(user=user)
        .select_related('achievement')
        .order_by('-earned_at')
    )
    achievements_data = [
        {
            "code": ua.achievement.slug,
            "name": ua.achievement.name,
            "description": ua.achievement.description,
            "icon": ua.achievement.icon,
            "badge_type": "gold" if ua.achievement.xp_bonus >= 100 else ("silver" if ua.achievement.xp_bonus >= 50 else "bronze"),
            "unlocked_at": ua.earned_at,
        }
        for ua in user_achievements
    ]

    # 5. Proof of Work Activity Stream
    recent_activity = (
        ActivityLog.objects.filter(user=user)
        .order_by('-created_at')[:8]
    )
    activity_data = [
        {
            "id": a.id,
            "activity_type": a.activity_type,
            "description": a.description,
            "created_at": a.created_at,
        }
        for a in recent_activity
    ]

    level_info = calculate_level(profile.total_xp)

    return {
        "user": {
            "username": user.username,
            "display_name": profile.display_name or user.username,
            "current_level": level_info['level'],
            "level_title": level_info['title'],
            "total_xp": profile.total_xp,
            "problems_solved_count": profile.problems_solved_count,
            "current_streak_days": profile.current_streak_days,
            "bio": getattr(profile, 'bio', '') or "Competitive programmer & full-stack software engineer.",
            "avatar_url": getattr(profile, 'avatar_url', '') or "",
            "phone_number": getattr(profile, 'phone_number', '') or "",
            "github_url": getattr(profile, 'github_url', '') or "",
            "linkedin_url": getattr(profile, 'linkedin_url', '') or "",
            "twitter_url": getattr(profile, 'twitter_url', '') or "",
            "website_url": getattr(profile, 'website_url', '') or "",
            "joined_at": user.date_joined,
        },
        "tracks": tracks_data,
        "verified_projects": verified_projects,
        "skill_domains": skill_domains,
        "achievements": achievements_data,
        "recent_activity": activity_data,
    }
