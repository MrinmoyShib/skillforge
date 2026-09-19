"""
Selectors for reading user progress, milestones, and solved challenges.
"""
from apps.accounts.models import UserProfile
from ..models import UserProgress, ActivityLog
from ..services.leveling import calculate_level


def get_user_progress_summary(user) -> dict:
    """
    Returns complete progress overview for a user including level tier and next XP milestone.
    """
    profile, _ = UserProfile.objects.get_or_create(user=user)
    level_info = calculate_level(profile.total_xp)

    return {
        "username": user.username,
        "display_name": profile.display_name or user.username,
        "total_xp": profile.total_xp,
        "current_level": level_info['level'],
        "level_title": level_info['title'],
        "current_level_base_xp": level_info['current_level_base_xp'],
        "next_level_xp": level_info['next_level_xp'],
        "progress_percent": level_info['progress_percent'],
        "problems_solved_count": profile.problems_solved_count,
        "current_streak_days": profile.current_streak_days,
        "last_solve_date": profile.last_solve_date,
    }


def get_user_solved_problem_ids(user) -> list[int]:
    """
    Returns a list of problem IDs successfully solved by the user.
    """
    return list(
        UserProgress.objects.filter(user=user, solved=True).values_list('problem_id', flat=True)
    )


def get_user_activity_feed(user, limit: int = 10):
    """
    Returns the recent activity milestones for a user.
    """
    return ActivityLog.objects.filter(user=user).order_by('-created_at')[:limit]

