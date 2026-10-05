"""
Unit tests for accounts services.
"""
import pytest
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.db import transaction
from apps.accounts.services.auth_services import (
    user_register,
    user_authenticate,
    user_generate_tokens,
    user_profile_update,
    token_blacklist_refresh,
    user_generate_otp,
)
from apps.accounts.models import UserProfile

User = get_user_model()


@pytest.mark.django_db
class TestAuthServices:
    def test_user_register_creates_user_and_profile(self):
        user = user_register(
            username="testdev",
            email="testdev@example.com",
            password="SecurePassword123!",
            display_name="Test Developer"
        )
        assert user.id is not None
        assert user.username == "testdev"
        assert user.email == "testdev@example.com"
        assert user.check_password("SecurePassword123!")

        profile = UserProfile.objects.get(user=user)
        assert profile.display_name == "Test Developer"
        assert profile.total_xp == 0
        assert profile.current_level == 1

    def test_user_register_default_display_name(self):
        user = user_register(
            username="coder99",
            email="coder99@example.com",
            password="SecurePassword123!"
        )
        profile = UserProfile.objects.get(user=user)
        assert profile.display_name == "coder99"

    def test_user_authenticate_with_username_and_email(self):
        user = user_register(
            username="alexsmith",
            email="alex@example.com",
            password="SecurePassword123!",
            is_active=True
        )
        # Auth via username
        auth_user_1 = user_authenticate(username="alexsmith", password="SecurePassword123!")
        assert auth_user_1 == user

        # Auth via email
        auth_user_2 = user_authenticate(username="alex@example.com", password="SecurePassword123!")
        assert auth_user_2 == user

        # Wrong password
        assert user_authenticate(username="alexsmith", password="WrongPassword") is None

    def test_user_generate_tokens_and_blacklist(self):
        user = user_register(
            username="tokenuser",
            email="token@example.com",
            password="SecurePassword123!"
        )
        access_token, refresh_token = user_generate_tokens(user=user)
        assert isinstance(access_token, str) and len(access_token) > 0
        assert isinstance(refresh_token, str) and len(refresh_token) > 0

        # Blacklist refresh token
        success = token_blacklist_refresh(refresh_token_str=refresh_token)
        assert success is True

    def test_user_profile_update(self):
        user = user_register(
            username="updateuser",
            email="update@example.com",
            password="SecurePassword123!"
        )
        profile = user_profile_update(
            user=user,
            display_name="Updated Name",
            bio="Building awesome things",
            location="Berlin, Germany"
        )
        assert profile.display_name == "Updated Name"
        assert profile.bio == "Building awesome things"
        assert profile.location == "Berlin, Germany"

    @pytest.mark.django_db(transaction=True)
    def test_user_otp_dispatch_on_commit_only(self):
        from unittest.mock import patch
        from django.db import transaction
        from apps.accounts.services.auth_services import user_generate_otp

        user = User.objects.create_user(username="txuser", email="txuser@example.com", password="password")

        with patch("apps.accounts.services.auth_services.send_otp_email_task.delay") as mock_delay:
            # 1. Rolled-back transaction should NOT dispatch task
            try:
                with transaction.atomic():
                    user_generate_otp(user)
                    raise RuntimeError("Simulated failure before commit")
            except RuntimeError:
                pass

            mock_delay.assert_not_called()

            # 2. Committed transaction DOES dispatch task
            with transaction.atomic():
                user_generate_otp(user)

            mock_delay.assert_called_once_with(
                email="txuser@example.com",
                username="txuser",
                otp_code=mock_delay.call_args[1]["otp_code"]
            )

    @pytest.mark.django_db(transaction=True)
    def test_user_otp_dispatch_fallback_to_sync_apply(self):
        user = User.objects.create_user(username="fallbackuser", email="fb@example.com", password="password")

        with patch("apps.accounts.services.auth_services.send_otp_email_task.delay", side_effect=Exception("Redis down")), \
             patch("apps.accounts.services.auth_services.send_otp_email_task.apply") as mock_apply:
            with transaction.atomic():
                code = user_generate_otp(user)

            mock_apply.assert_called_once_with(kwargs={
                "email": "fb@example.com",
                "username": "fallbackuser",
                "otp_code": code,
            })

    def test_user_authenticate_case_insensitive_username(self):
        User.objects.create_user(username="AliceDev", email="alice@example.com", password="SecurePassword123!")
        
        # Exact match
        auth_exact = user_authenticate(username="AliceDev", password="SecurePassword123!")
        assert auth_exact is not None
        assert auth_exact.username == "AliceDev"

        # Lowercase match
        auth_lower = user_authenticate(username="alicedev", password="SecurePassword123!")
        assert auth_lower is not None
        assert auth_lower.username == "AliceDev"

        # Uppercase match
        auth_upper = user_authenticate(username="ALICEDEV", password="SecurePassword123!")
        assert auth_upper is not None
        assert auth_upper.username == "AliceDev"

