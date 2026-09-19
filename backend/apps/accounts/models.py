from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=150, blank=True)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    github_url = models.URLField(max_length=255, blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True)
    twitter_url = models.URLField(max_length=255, blank=True)
    website_url = models.URLField(max_length=255, blank=True)
    total_xp = models.IntegerField(default=0, db_index=True)
    current_level = models.IntegerField(default=1)
    problems_solved_count = models.IntegerField(default=0)
    current_streak_days = models.IntegerField(default=0)
    last_solve_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class EmailVerificationOTP(models.Model):
    """
    Stores 6-digit OTP codes for email verification with rate-limiting and expiration.
    Supports both new account registration and secure email address changes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_otps')
    otp_code = models.CharField(max_length=6)
    new_email = models.EmailField(blank=True, default='')
    purpose = models.CharField(max_length=20, default='registration')  # 'registration' | 'email_change'
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_used']),
            models.Index(fields=['user', 'purpose', 'is_used']),
        ]

    def is_valid(self) -> bool:
        return not self.is_used and self.attempts < 5 and timezone.now() <= self.expires_at

    def __str__(self):
        target = self.new_email or self.user.email
        return f"OTP for {target} [{self.purpose}] (expires {self.expires_at})"

