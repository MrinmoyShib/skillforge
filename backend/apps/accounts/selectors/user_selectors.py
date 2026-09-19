"""
Selectors (database reads) for accounts and user profiles.
"""
from typing import Optional
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


def user_get_by_id(*, user_id: int) -> Optional[User]:
    """
    Fetches a user by ID with their profile pre-fetched.
    """
    return User.objects.filter(id=user_id, is_active=True).select_related('profile').first()


def user_get_by_username(*, username: str) -> Optional[User]:
    """
    Fetches a user by username (case-insensitive) with profile.
    """
    return User.objects.filter(username__iexact=username, is_active=True).select_related('profile').first()


def user_list_active() -> QuerySet[User]:
    """
    Returns all active users with profile preloaded.
    """
    return User.objects.filter(is_active=True).select_related('profile').order_by('-date_joined')

