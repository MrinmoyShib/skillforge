"""
Models for Coding Problems, Categories, Tags, and TestCases.
"""
from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class DifficultyXPConfig(models.Model):
    """
    Lookup table for configurable XP rewards per difficulty level.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, unique=True)
    xp_reward = models.PositiveIntegerField(help_text="XP awarded for solving a problem of this difficulty")

    class Meta:
        verbose_name = "Difficulty XP Configuration"
        verbose_name_plural = "Difficulty XP Configurations"

    def __str__(self):
        return f"{self.get_difficulty_display()}: {self.xp_reward} XP"


class Category(TimeStampedModel):
    """
    Problem taxonomy category (e.g. Arrays, Strings, Dynamic Programming).
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    """
    Tags for fine-grained problem classification (e.g. two-pointers, sliding-window).
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Problem(TimeStampedModel):
    """
    Coding challenge definition.
    """
    DIFFICULTY_EASY = 'easy'
    DIFFICULTY_MEDIUM = 'medium'
    DIFFICULTY_HARD = 'hard'

    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, 'Easy'),
        (DIFFICULTY_MEDIUM, 'Medium'),
        (DIFFICULTY_HARD, 'Hard'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(help_text="Full markdown problem description")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, db_index=True)
    challenge_level = models.PositiveSmallIntegerField(
        default=1,
        help_text="Progression tier from 1 (Beginner) to 5 (Expert)",
        db_index=True
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='problems')
    tags = models.ManyToManyField(Tag, blank=True, related_name='problems')
    xp_reward = models.PositiveIntegerField(default=50, help_text="XP awarded on first accepted solve")
    
    constraints = models.TextField(blank=True, help_text="Constraints on inputs and bounds")
    input_format = models.TextField(blank=True, help_text="Input stream format specification")
    output_format = models.TextField(blank=True, help_text="Expected output format specification")
    examples = models.JSONField(default=list, blank=True, help_text="List of example inputs, outputs, and explanations")
    
    starter_code = models.TextField(blank=True, help_text="Initial C++ boilerplate provided to the user")
    language = models.CharField(max_length=50, default='cpp', help_text="Target programming language")
    time_limit_seconds = models.FloatField(default=2.0, help_text="Maximum CPU time limit in seconds")
    memory_limit_kb = models.PositiveIntegerField(default=262144, help_text="Memory limit in KB (256 MB)")
    
    is_published = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['challenge_level', 'id']
        indexes = [
            models.Index(fields=['difficulty', 'is_published']),
            models.Index(fields=['challenge_level', 'is_published']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.title}"


class TestCase(TimeStampedModel):
    """
    Test cases for evaluating problem submissions.
    Sample cases are visible to learners; hidden cases are used for evaluation only.
    """
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField(help_text="Standard input provided to the program")
    expected_output = models.TextField(help_text="Exact standard output expected")
    is_sample = models.BooleanField(default=False, help_text="If true, visible on the problem page as an example")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        case_type = "Sample" if self.is_sample else "Hidden"
        return f"{case_type} Case #{self.id} for {self.problem.title}"


TestCase.__test__ = False
