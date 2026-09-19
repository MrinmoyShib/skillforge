from django.db import models
from django.conf import settings
from django.utils import timezone


class LevelRequirement(models.Model):
    """
    Lookup table defining XP thresholds and titles for each skill level tier.
    """
    level = models.PositiveIntegerField(unique=True)
    xp_threshold = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=64, default="Coder")

    class Meta:
        ordering = ['level']
        verbose_name = "Level Requirement"
        verbose_name_plural = "Level Requirements"

    def __str__(self):
        return f"Level {self.level} ({self.title}) — {self.xp_threshold} XP"


class UserProgress(models.Model):
    """
    Tracks per-user problem solve status.
    Guarantees anti-farming rule at the database level via a unique constraint.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_records'
    )
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='progress_records'
    )
    solved = models.BooleanField(default=True)
    xp_awarded = models.PositiveIntegerField(default=0)
    best_submission = models.ForeignKey(
        'submissions.Submission',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    first_solved_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'problem'],
                name='unique_user_problem_progress'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'solved']),
            models.Index(fields=['problem', 'solved']),
        ]
        verbose_name = "User Progress"
        verbose_name_plural = "User Progress Records"

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} (Solved: {self.solved})"


class ActivityLog(models.Model):
    """
    Timeline log of user milestones (solves, level ups, achievements).
    """
    class ActivityType(models.TextChoices):
        SOLVE = 'SOLVE', 'Solved Problem'
        LEVEL_UP = 'LEVEL_UP', 'Level Up'
        SUBMISSION = 'SUBMISSION', 'Submission'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.CharField(
        max_length=32,
        choices=ActivityType.choices,
        default=ActivityType.SOLVE
    )
    description = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.user.username}: {self.description} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

