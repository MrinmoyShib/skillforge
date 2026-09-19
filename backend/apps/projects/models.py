"""
Models for Guided Projects, Project Milestones, and User Project Progress.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Project(TimeStampedModel):
    """
    Real-world software engineering guided project.
    """
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('cpp', 'C++'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, default='python', db_index=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium', db_index=True)
    challenge_level = models.PositiveSmallIntegerField(default=2, help_text="Skill level tier (1-5)")
    short_description = models.CharField(max_length=500)
    description = models.TextField(help_text="Detailed markdown project brief, architecture overview, and goals")
    technologies = models.JSONField(default=list, blank=True, help_text="List of tech tags (e.g. ['Node.js', 'EventLoop'])")
    starter_files = models.JSONField(default=dict, blank=True, help_text="Dictionary of filename to initial boilerplate")
    xp_reward = models.PositiveIntegerField(default=150, help_text="Bonus XP awarded upon project completion")
    estimated_minutes = models.PositiveIntegerField(default=60, help_text="Estimated time to complete")
    is_published = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Guided Project"
        verbose_name_plural = "Guided Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_language_display()}] {self.title}"


class ProjectMilestone(TimeStampedModel):
    """
    A single verification step / milestone in a guided project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    order = models.PositiveIntegerField(default=1, help_text="Step order within the project (1, 2, 3...)")
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Markdown step requirements and architectural specifications")
    starter_code = models.TextField(blank=True, help_text="Code skeleton for this milestone")
    test_harness_code = models.TextField(help_text="Verification test runner code executed in the sandbox")
    hints = models.JSONField(default=list, blank=True, help_text="List of progressive guidance hints")
    xp_reward = models.PositiveIntegerField(default=50, help_text="XP awarded when this milestone passes")

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('project', 'order')
        verbose_name = "Project Milestone"
        verbose_name_plural = "Project Milestones"

    def __str__(self):
        return f"{self.project.title} — Milestone #{self.order}: {self.title}"


class UserProjectProgress(TimeStampedModel):
    """
    Tracks a student's enrollment, milestone completions, and submitted code for a project.
    """
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_progress')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='IN_PROGRESS', db_index=True)
    current_milestone_order = models.PositiveIntegerField(default=1)
    completed_milestones = models.JSONField(default=list, blank=True, help_text="List of completed milestone IDs")
    submitted_code = models.JSONField(default=dict, blank=True, help_text="Mapping of milestone_id to code string")
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'project')
        verbose_name = "User Project Progress"
        verbose_name_plural = "User Project Progress Records"

    def __str__(self):
        return f"{self.user.username} — {self.project.title} [{self.status}]"

