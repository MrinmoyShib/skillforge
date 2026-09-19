"""
Transactional services for problem completion, anti-farming enforcement, and activity logging.
"""
import logging
from django.db import transaction
from django.utils import timezone
from apps.accounts.models import UserProfile
from ..models import UserProgress, ActivityLog
from .leveling import calculate_level

logger = logging.getLogger(__name__)


def record_problem_solved(*, user, problem, submission) -> int:
    """
    Records a problem solve, awards XP, updates streaks, checks level advancement,
    and creates timeline activity records.

    Anti-Farming Rule (§10.4):
    Guarantees XP is awarded at most ONCE per user per problem using atomic DB constraints.
    """
    with transaction.atomic():
        progress, created = UserProgress.objects.get_or_create(
            user=user,
            problem=problem,
            defaults={
                'solved': True,
                'xp_awarded': problem.xp_reward,
                'best_submission': submission,
                'first_solved_at': submission.created_at if submission else timezone.now(),
            }
        )

        if not created:
            # Already solved previously — do not grant duplicate XP
            logger.info(f"User {user.username} re-solved {problem.title}. No duplicate XP awarded (anti-farming).")
            return 0

        # Update profile stats with row-level lock
        profile = UserProfile.objects.select_for_update().get(user=user)
        old_level = profile.current_level

        xp_gained = problem.xp_reward
        profile.total_xp += xp_gained
        profile.problems_solved_count += 1

        # Streak calculation
        today = timezone.now().date()
        if profile.last_solve_date != today:
            if profile.last_solve_date and (today - profile.last_solve_date).days == 1:
                profile.current_streak_days += 1
            else:
                profile.current_streak_days = 1
            profile.last_solve_date = today

        # Recalculate level
        level_info = calculate_level(profile.total_xp)
        new_level = level_info['level']
        profile.current_level = new_level
        profile.save(update_fields=['total_xp', 'problems_solved_count', 'current_streak_days', 'last_solve_date', 'current_level'])

        # Log Activity: Solved Problem
        ActivityLog.objects.create(
            user=user,
            activity_type=ActivityLog.ActivityType.SOLVE,
            description=f"Solved {problem.title} (+{xp_gained} XP)",
            metadata={
                "problem_id": problem.id,
                "problem_slug": problem.slug,
                "xp_awarded": xp_gained,
                "difficulty": problem.difficulty,
            }
        )

        # Log Activity: Level Up
        if new_level > old_level:
            ActivityLog.objects.create(
                user=user,
                activity_type=ActivityLog.ActivityType.LEVEL_UP,
                description=f"Leveled up to Level {new_level} — {level_info['title']}!",
                metadata={
                    "level": new_level,
                    "title": level_info['title'],
                    "total_xp": profile.total_xp
                }
            )
        # Check and grant any newly unlocked achievements
        try:
            from apps.achievements.services.achievement_engine import check_and_grant_achievements
            check_and_grant_achievements(user)
        except Exception as e:
            logger.warning(f"Error checking achievements for {user.username}: {e}")

        logger.info(f"Awarded {xp_gained} XP to {user.username} for solving {problem.title}.")
        return xp_gained

