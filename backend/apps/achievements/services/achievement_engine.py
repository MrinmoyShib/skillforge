"""
Automated achievement evaluation and granting engine.
"""
import logging
from django.db import transaction
from django.db.models import Count
from apps.progress.models import UserProgress, ActivityLog
from ..models import Achievement, UserAchievement

logger = logging.getLogger(__name__)


def check_and_grant_achievements(user) -> list[Achievement]:
    """
    Evaluates all unearned achievements for a user against their latest telemetry
    and grants any newly satisfied badges atomically.
    """
    from apps.accounts.models import UserProfile
    profile = UserProfile.objects.filter(user=user).first()
    if not profile:
        return []

    newly_granted = []

    with transaction.atomic():
        earned_ids = set(
            UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
        )
        unearned_achievements = list(Achievement.objects.exclude(id__in=earned_ids))

        if not unearned_achievements:
            return []

        # Gather user metrics
        solved_count = profile.problems_solved_count
        streak_days = profile.current_streak_days
        current_level = profile.current_level

        # Category solves map: {category_id: solved_count}
        cat_counts = (
            UserProgress.objects.filter(user=user, solved=True, problem__is_published=True)
            .values('problem__category_id')
            .annotate(count=Count('id'))
        )
        category_solves_map = {item['problem__category_id']: item['count'] for item in cat_counts}

        bonus_xp_total = 0

        for ach in unearned_achievements:
            eligible = False

            if ach.criteria_type == Achievement.CriteriaType.FIRST_SOLVE:
                eligible = solved_count >= 1
            elif ach.criteria_type == Achievement.CriteriaType.PROBLEMS_COUNT:
                eligible = solved_count >= ach.criteria_value
            elif ach.criteria_type == Achievement.CriteriaType.STREAK_DAYS:
                eligible = streak_days >= ach.criteria_value
            elif ach.criteria_type == Achievement.CriteriaType.LEVEL_REACHED:
                eligible = current_level >= ach.criteria_value
            elif ach.criteria_type == Achievement.CriteriaType.CATEGORY_SOLVE:
                cat_solved = category_solves_map.get(ach.criteria_category_id, 0)
                eligible = cat_solved >= ach.criteria_value

            if eligible:
                UserAchievement.objects.create(user=user, achievement=ach)
                newly_granted.append(ach)

                if ach.xp_bonus > 0:
                    bonus_xp_total += ach.xp_bonus

                # Log to user activity feed
                ActivityLog.objects.create(
                    user=user,
                    activity_type=ActivityLog.ActivityType.LEVEL_UP if ach.criteria_type == Achievement.CriteriaType.LEVEL_REACHED else ActivityLog.ActivityType.SOLVE,
                    description=f"Unlocked Achievement: {ach.icon} {ach.name}!",
                    metadata={
                        "achievement_id": ach.id,
                        "achievement_name": ach.name,
                        "achievement_slug": ach.slug,
                        "icon": ach.icon,
                        "xp_bonus": ach.xp_bonus
                    }
                )
                logger.info(f"Granted achievement '{ach.name}' to user {user.username}.")

        if bonus_xp_total > 0:
            profile.total_xp += bonus_xp_total
            profile.save(update_fields=['total_xp'])

    return newly_granted
