"""
Selectors for querying achievements with user unlock status and progress.
"""
from django.db.models import Count
from apps.progress.models import UserProgress
from ..models import Achievement, UserAchievement


def get_user_achievements_with_status(user) -> list[dict]:
    """
    Returns all achievements annotated with the user's unlocked status,
    unlock timestamp, and current progress toward unlocking.
    """
    achievements = Achievement.objects.all().order_by('id')

    if not user or not user.is_authenticated:
        return [
            {
                "id": ach.id,
                "name": ach.name,
                "slug": ach.slug,
                "description": ach.description,
                "icon": ach.icon,
                "criteria_type": ach.criteria_type,
                "criteria_value": ach.criteria_value,
                "xp_bonus": ach.xp_bonus,
                "is_unlocked": False,
                "earned_at": None,
                "current_progress": 0,
                "progress_percent": 0.0,
            }
            for ach in achievements
        ]

    from apps.accounts.models import UserProfile
    profile = UserProfile.objects.filter(user=user).first()
    solved_count = profile.problems_solved_count if profile else 0
    streak_days = profile.current_streak_days if profile else 0
    current_level = profile.current_level if profile else 1

    cat_counts = (
        UserProgress.objects.filter(user=user, solved=True, problem__is_published=True)
        .values('problem__category_id')
        .annotate(count=Count('id'))
    )
    category_solves_map = {item['problem__category_id']: item['count'] for item in cat_counts}

    earned_grants = {
        ua.achievement_id: ua.earned_at
        for ua in UserAchievement.objects.filter(user=user)
    }

    results = []
    for ach in achievements:
        is_unlocked = ach.id in earned_grants
        earned_at = earned_grants.get(ach.id)

        # Calculate progress
        if is_unlocked:
            current_progress = ach.criteria_value
            progress_percent = 100.0
        else:
            if ach.criteria_type == Achievement.CriteriaType.FIRST_SOLVE:
                current_progress = min(1, solved_count)
            elif ach.criteria_type == Achievement.CriteriaType.PROBLEMS_COUNT:
                current_progress = min(ach.criteria_value, solved_count)
            elif ach.criteria_type == Achievement.CriteriaType.STREAK_DAYS:
                current_progress = min(ach.criteria_value, streak_days)
            elif ach.criteria_type == Achievement.CriteriaType.LEVEL_REACHED:
                current_progress = min(ach.criteria_value, current_level)
            elif ach.criteria_type == Achievement.CriteriaType.CATEGORY_SOLVE:
                cat_solved = category_solves_map.get(ach.criteria_category_id, 0)
                current_progress = min(ach.criteria_value, cat_solved)
            else:
                current_progress = 0

            target = max(1, ach.criteria_value)
            progress_percent = round(min(100.0, (current_progress / target) * 100.0), 1)

        results.append({
            "id": ach.id,
            "name": ach.name,
            "slug": ach.slug,
            "description": ach.description,
            "icon": ach.icon,
            "criteria_type": ach.criteria_type,
            "criteria_value": ach.criteria_value,
            "xp_bonus": ach.xp_bonus,
            "is_unlocked": is_unlocked,
            "earned_at": earned_at,
            "current_progress": current_progress,
            "progress_percent": progress_percent,
        })

    return results
