"""
Unit tests for accounts services.
"""
import pytest
from django.contrib.auth import get_user_model
from apps.accounts.services.auth_services import (
    user_register,
    user_authenticate,
    user_generate_tokens,
    user_profile_update,
    token_blacklist_refresh,
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
            password="SecurePassword123!"
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

