from django.db import models
from django.conf import settings
from django.utils import timezone


class Achievement(models.Model):
    """
    Catalog of platform badges and milestone achievements.
    """
    class CriteriaType(models.TextChoices):
        FIRST_SOLVE = 'FIRST_SOLVE', 'First Problem Solved'
        PROBLEMS_COUNT = 'PROBLEMS_COUNT', 'Total Problems Solved'
        CATEGORY_SOLVE = 'CATEGORY_SOLVE', 'Problems Solved in Category'
        STREAK_DAYS = 'STREAK_DAYS', 'Daily Streak Days'
        LEVEL_REACHED = 'LEVEL_REACHED', 'Skill Level Milestone'

    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=32, default="🏆")
    criteria_type = models.CharField(max_length=32, choices=CriteriaType.choices)
    criteria_value = models.PositiveIntegerField(default=1)
    criteria_category = models.ForeignKey(
        'problems.Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    xp_bonus = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criteria_value', 'id']
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

    def __str__(self):
        return f"{self.icon} {self.name} ({self.criteria_type}={self.criteria_value})"


class UserAchievement(models.Model):
    """
    Records an earned achievement for a user.
    Database-level uniqueness prevents duplicate grants.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_achievements'
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name='user_grants'
    )
    earned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'achievement'],
                name='unique_user_achievement'
            )
        ]
        indexes = [
            models.Index(fields=['user', '-earned_at']),
        ]
        ordering = ['-earned_at']
        verbose_name = "User Achievement"
        verbose_name_plural = "User Achievements"

    def __str__(self):
        return f"{self.user.username} earned {self.achievement.name}"

