"""
Business logic and mutations for authentication and user management.
"""
from typing import Optional, Tuple
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import UserProfile

User = get_user_model()


def user_register(
    *,
    username: str,
    email: str,
    password: str,
    display_name: str = ""
) -> User:
    """
    Creates a new User and initializes their UserProfile atomically.
    """
    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        effective_display_name = display_name.strip() if display_name else username
        UserProfile.objects.create(
            user=user,
            display_name=effective_display_name,
        )

        return user


def user_authenticate(
    *,
    username: str,
    password: str
) -> Optional[User]:
    """
    Authenticates a user via username or email with password.
    """
    # Check if input is email
    if '@' in username:
        user_obj = User.objects.filter(email__iexact=username).first()
        if user_obj:
            username = user_obj.username

    return authenticate(username=username, password=password)


def user_generate_tokens(*, user: User) -> Tuple[str, str]:
    """
    Generates a fresh (access_token, refresh_token) pair for the user.
    """
    refresh = RefreshToken.for_user(user)
    # Add custom claims if needed (e.g. is_staff)
    refresh['is_staff'] = user.is_staff
    return str(refresh.access_token), str(refresh)


def user_profile_update(
    *,
    user: User,
    username: Optional[str] = None,
    email: Optional[str] = None,
    display_name: Optional[str] = None,
    phone_number: Optional[str] = None,
    bio: Optional[str] = None,
    location: Optional[str] = None,
    avatar_url: Optional[str] = None,
    github_url: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    twitter_url: Optional[str] = None,
    website_url: Optional[str] = None,
) -> UserProfile:
    """
    Updates mutable user and profile fields atomically.
    """
    with transaction.atomic():
        user_update_fields = []
        if username is not None and username.strip():
            user.username = username.strip()
            user_update_fields.append('username')
        if email is not None and email.strip():
            user.email = email.strip().lower()
            user_update_fields.append('email')
        if user_update_fields:
            user.save(update_fields=user_update_fields)

        profile, _ = UserProfile.objects.select_for_update().get_or_create(user=user)
        profile_update_fields = []

        if display_name is not None:
            profile.display_name = display_name
            profile_update_fields.append('display_name')
        if phone_number is not None:
            profile.phone_number = phone_number
            profile_update_fields.append('phone_number')
        if bio is not None:
            profile.bio = bio
            profile_update_fields.append('bio')
        if location is not None:
            profile.location = location
            profile_update_fields.append('location')
        if avatar_url is not None:
            profile.avatar_url = avatar_url
            profile_update_fields.append('avatar_url')
        if github_url is not None:
            profile.github_url = github_url
            profile_update_fields.append('github_url')
        if linkedin_url is not None:
            profile.linkedin_url = linkedin_url
            profile_update_fields.append('linkedin_url')
        if twitter_url is not None:
            profile.twitter_url = twitter_url
            profile_update_fields.append('twitter_url')
        if website_url is not None:
            profile.website_url = website_url
            profile_update_fields.append('website_url')

        if profile_update_fields:
            profile_update_fields.append('updated_at')
            profile.save(update_fields=profile_update_fields)

        return profile


def user_change_password(*, user: User, new_password: str) -> None:
    """
    Sets a new password for the user and saves it.
    """
    user.set_password(new_password)
    user.save(update_fields=['password'])


def token_blacklist_refresh(*, refresh_token_str: str) -> bool:
    """
    Blacklists a refresh token to prevent replay attacks.
    """
    try:
        token = RefreshToken(refresh_token_str)
        token.blacklist()
        return True
    except Exception:
        return False

