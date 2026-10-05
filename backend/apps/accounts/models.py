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

    class Meta:
        indexes = [
            models.Index(fields=['-total_xp', '-problems_solved_count', 'id'], name='idx_profile_xp_rank'),
            models.Index(fields=['-problems_solved_count', '-total_xp', 'id'], name='idx_profile_solved_rank'),
        ]

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def active_streak_days(self) -> int:
        """
        Dynamically calculates active streak length, resetting to 0 if the user
        has been inactive for more than 1 day since their last solve.
        """
        if self.current_streak_days <= 0:
            return 0
        if not self.last_solve_date:
            return self.current_streak_days
        from django.utils import timezone
        today = timezone.now().date()
        days_diff = (today - self.last_solve_date).days
        if days_diff > 1:
            return 0
        return self.current_streak_days


class EmailVerificationOTP(models.Model):
    """
    Stores 6-digit OTP codes for email verification with rate-limiting and expiration.
    Supports both new account registration and secure email address changes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_otps')
    otp_code = models.CharField(max_length=128)
    new_email = models.EmailField(blank=True, default='')
    purpose = models.CharField(max_length=20, default='registration')  # 'registration' | 'email_change'
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_used'], name='accounts_em_user_id_449622_idx'),
            models.Index(fields=['user', 'purpose', 'is_used'], name='accounts_em_user_id_c91823_idx'),
        ]

    def set_otp(self, raw_code: str):
        from django.contrib.auth.hashers import make_password
        self.otp_code = make_password(raw_code)

    def check_otp(self, raw_code: str) -> bool:
        from django.contrib.auth.hashers import check_password
        if check_password(raw_code, self.otp_code):
            return True
        return self.otp_code == raw_code

    def is_valid(self) -> bool:
        return not self.is_used and self.attempts < 5 and timezone.now() <= self.expires_at

    def __str__(self):
        target = self.new_email or self.user.email
        return f"OTP for {target} [{self.purpose}] (expires {self.expires_at})"

