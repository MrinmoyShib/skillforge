"""
Business logic and mutations for authentication and user management.
"""
import secrets
from datetime import timedelta
from typing import Optional, Tuple
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction, IntegrityError
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from ..models import UserProfile, EmailVerificationOTP
from ..tasks import (
    send_otp_email_task,
    send_email_change_otp_task,
    send_email_changed_security_alert_task,
)

User = get_user_model()


def user_generate_otp(user: User) -> str:
    """
    Generates a secure 6-digit OTP, stores it in EmailVerificationOTP,
    and dispatches a Celery task to email it to the user.
    """
    code = f"{secrets.randbelow(900000) + 100000}"
    expires_at = timezone.now() + timedelta(minutes=10)

    EmailVerificationOTP.objects.create(
        user=user,
        otp_code=code,
        expires_at=expires_at,
    )

    # Dispatch asynchronous email task
    try:
        send_otp_email_task.delay(
            email=user.email,
            username=user.username,
            otp_code=code
        )
    except Exception:
        # Fallback to synchronous if Celery broker is unavailable in dev
        send_otp_email_task(
            email=user.email,
            username=user.username,
            otp_code=code
        )

    return code


def user_register(
    *,
    username: str,
    email: str,
    password: str,
    display_name: str = "",
    is_active: bool = False
) -> User:
    """
    Creates a new User, initializes their UserProfile,
    and sends a 6-digit email verification OTP if inactive.
    """
    normalized_email = email.lower().strip() if email else ""

    with transaction.atomic():
        user = User.objects.create_user(
            username=username.strip(),
            email=normalized_email,
            password=password,
            is_active=is_active
        )

        effective_display_name = display_name.strip() if display_name else username.strip()
        UserProfile.objects.create(
            user=user,
            display_name=effective_display_name,
        )

        # Generate and save OTP only if user is inactive (e.g. registration flow)
        if not is_active:
            user_generate_otp(user)

        return user


def user_verify_otp(*, email: str, otp: str = "", otp_code: str = "") -> User:
    """
    Verifies a user's 6-digit OTP, marks the OTP as used,
    and activates the user account.
    """
    code_to_check = (otp or otp_code).strip()
    normalized_email = email.lower().strip()
    user = User.objects.filter(email__iexact=normalized_email).first()
    if not user:
        raise ValidationError({'detail': 'No account found with this email address.'})

    if user.is_active:
        return user

    otp_record = (
        EmailVerificationOTP.objects
        .filter(user=user, is_used=False)
        .order_by('-created_at')
        .first()
    )

    if not otp_record or not otp_record.is_valid():
        raise ValidationError({
            'detail': 'Verification code has expired or maximum attempts exceeded. Please request a new code.'
        })

    if otp_record.otp_code != code_to_check:
        otp_record.attempts += 1
        otp_record.save(update_fields=['attempts'])
        remaining = 5 - otp_record.attempts
        if remaining <= 0:
            raise ValidationError({
                'detail': 'Maximum verification attempts exceeded. Please request a new code.'
            })
        raise ValidationError({
            'detail': f'Invalid verification code. {remaining} attempt(s) remaining.'
        })

    # OTP is valid — activate account and mark code as used
    with transaction.atomic():
        otp_record.is_used = True
        otp_record.save(update_fields=['is_used'])

        user.is_active = True
        user.save(update_fields=['is_active'])

    return user


def user_resend_otp(*, email: str) -> None:
    """
    Generates and sends a new OTP for an inactive user,
    enforcing a 60-second cooldown period.
    """
    normalized_email = email.lower().strip()
    user = User.objects.filter(email__iexact=normalized_email).first()
    if not user:
        raise ValidationError({'detail': 'No account found with this email address.'})

    if user.is_active:
        raise ValidationError({'detail': 'This account is already verified. Please log in.'})

    # Enforce 60-second cooldown
    last_otp = (
        EmailVerificationOTP.objects
        .filter(user=user)
        .order_by('-created_at')
        .first()
    )
    if last_otp:
        elapsed = (timezone.now() - last_otp.created_at).total_seconds()
        if elapsed < 60:
            remaining = int(60 - elapsed)
            raise ValidationError({
                'detail': f'Please wait {remaining} second(s) before requesting another code.'
            })

    # Invalidate previous unused codes and generate new one
    EmailVerificationOTP.objects.filter(user=user, is_used=False).update(is_used=True)
    user_generate_otp(user)


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
        if user_update_fields:
            try:
                user.save(update_fields=user_update_fields)
            except IntegrityError:
                raise ValidationError({'detail': 'Username already taken.'})

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


def user_request_email_change(
    *,
    user: User,
    new_email: str,
    current_password: str
) -> str:
    """
    Validates current password and new email, enforces 60-second cooldown,
    generates a 6-digit OTP, and emails it to the new address.
    """
    if not user.check_password(current_password):
        raise ValidationError({'current_password': 'Current password is incorrect.'})

    normalized_new_email = new_email.lower().strip()
    if normalized_new_email == user.email.lower().strip():
        raise ValidationError({'new_email': 'New email must be different from your current email.'})

    if User.objects.filter(email__iexact=normalized_new_email).exclude(id=user.id).exists():
        raise ValidationError({'new_email': 'A user with that email already exists.'})

    # Enforce 60-second cooldown
    last_otp = (
        EmailVerificationOTP.objects
        .filter(user=user, purpose='email_change')
        .order_by('-created_at')
        .first()
    )
    if last_otp:
        elapsed = (timezone.now() - last_otp.created_at).total_seconds()
        if elapsed < 60:
            remaining = int(60 - elapsed)
            raise ValidationError({
                'detail': f'Please wait {remaining} second(s) before requesting another code.'
            })

    # Invalidate previous unused email change codes
    EmailVerificationOTP.objects.filter(user=user, purpose='email_change', is_used=False).update(is_used=True)

    code = f"{secrets.randbelow(900000) + 100000}"
    expires_at = timezone.now() + timedelta(minutes=10)

    EmailVerificationOTP.objects.create(
        user=user,
        otp_code=code,
        new_email=normalized_new_email,
        purpose='email_change',
        expires_at=expires_at,
    )

    try:
        send_email_change_otp_task.delay(
            new_email=normalized_new_email,
            username=user.username,
            otp_code=code
        )
    except Exception:
        send_email_change_otp_task(
            new_email=normalized_new_email,
            username=user.username,
            otp_code=code
        )

    return code


def user_confirm_email_change(
    *,
    user: User,
    new_email: str,
    otp: str = "",
    otp_code: str = ""
) -> Tuple[User, str]:
    """
    Verifies the 6-digit OTP sent to new_email, updates user.email,
    marks OTP as used, and dispatches a security alert to old_email.
    """
    code_to_check = (otp or otp_code).strip()
    normalized_new_email = new_email.lower().strip()

    if User.objects.filter(email__iexact=normalized_new_email).exclude(id=user.id).exists():
        raise ValidationError({'new_email': 'A user with that email already exists.'})

    otp_record = (
        EmailVerificationOTP.objects
        .filter(user=user, new_email__iexact=normalized_new_email, purpose='email_change', is_used=False)
        .order_by('-created_at')
        .first()
    )

    if not otp_record or not otp_record.is_valid():
        raise ValidationError({
            'detail': 'Verification code has expired or maximum attempts exceeded. Please request a new code.'
        })

    if otp_record.otp_code != code_to_check:
        otp_record.attempts += 1
        otp_record.save(update_fields=['attempts'])
        remaining = 5 - otp_record.attempts
        if remaining <= 0:
            raise ValidationError({
                'detail': 'Maximum verification attempts exceeded. Please request a new code.'
            })
        raise ValidationError({
            'detail': f'Invalid verification code. {remaining} attempt(s) remaining.'
        })

    old_email = user.email

    with transaction.atomic():
        otp_record.is_used = True
        otp_record.save(update_fields=['is_used'])

        user.email = normalized_new_email
        user.save(update_fields=['email'])

    # Send security alert to old email
    try:
        send_email_changed_security_alert_task.delay(
            old_email=old_email,
            username=user.username,
            new_email=normalized_new_email
        )
    except Exception:
        send_email_changed_security_alert_task(
            old_email=old_email,
            username=user.username,
            new_email=normalized_new_email
        )

    return user, old_email


def user_change_password(*, user: User, new_password: str) -> None:
    """
    Sets a new password for the user and saves it.
    """
    user.set_password(new_password)
    user.save(update_fields=['password'])

    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        BlacklistedToken.objects.get_or_create(token=token)


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

