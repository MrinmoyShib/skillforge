"""
Query-driven selectors for global and time-filtered leaderboard rankings.
"""
from apps.accounts.models import UserProfile
from apps.progress.services.leveling import calculate_level


def get_global_leaderboard(
    *,
    sort_by: str = 'xp',
    current_user=None,
    limit: int = 50,
    offset: int = 0
) -> dict:
    """
    Computes real-time, query-driven rankings across all active developers.
    """
    qs = UserProfile.objects.select_related('user').filter(user__is_active=True)

    if sort_by == 'solved':
        qs = qs.order_by('-problems_solved_count', '-total_xp', 'id')
    else:
        qs = qs.order_by('-total_xp', '-problems_solved_count', 'id')

    total_count = qs.count()
    paginated_slice = list(qs[offset:offset + limit])

    results = []
    for i, profile in enumerate(paginated_slice):
        rank = offset + i + 1
        level_info = calculate_level(profile.total_xp)

        results.append({
            "rank": rank,
            "user_id": profile.user.id,
            "username": profile.user.username,
            "display_name": profile.display_name or profile.user.username,
            "avatar_initial": (profile.display_name or profile.user.username or "U")[0].toUpperCase() if hasattr(str, 'toUpperCase') else (profile.display_name or profile.user.username or "U")[0].upper(),
            "level": level_info['level'],
            "level_title": level_info['title'],
            "total_xp": profile.total_xp,
            "problems_solved_count": profile.problems_solved_count,
            "current_streak_days": profile.current_streak_days,
            "is_current_user": bool(current_user and current_user.is_authenticated and profile.user_id == current_user.id),
        })

    # Calculate exact standing of current user if logged in
    current_user_rank = None
    if current_user and current_user.is_authenticated:
        try:
            curr_profile = current_user.profile
            if sort_by == 'solved':
                better_users_count = qs.filter(
                    problems_solved_count__gt=curr_profile.problems_solved_count
                ).count()
            else:
                better_users_count = qs.filter(
                    total_xp__gt=curr_profile.total_xp
                ).count()
            current_user_rank = better_users_count + 1
        except Exception:
            current_user_rank = None

    return {
        "results": results,
        "total_count": total_count,
        "current_user_rank": current_user_rank,
    }

