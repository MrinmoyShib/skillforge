"""
Celery asynchronous tasks for user account operations (e.g., OTP email delivery).
"""
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_otp_email_task(self, email: str, username: str, otp_code: str):
    """
    Asynchronously sends a 6-digit verification code email for account registration.
    """
    subject = f"SkillForge — Your Verification Code: {otp_code}"
    message = (
        f"Hi {username},\n\n"
        f"Welcome to SkillForge!\n\n"
        f"Your 6-digit verification code is: {otp_code}\n\n"
        f"This code will expire in 10 minutes.\n\n"
        f"If you did not request this code, you can safely ignore this email.\n\n"
        f"— The SkillForge Team"
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SkillForge <noreply@skillforge.dev>')

    try:
        logger.info(f"Sending OTP verification email to {email}")
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"OTP verification email successfully sent to {email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send OTP email to {email}: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_email_change_otp_task(self, new_email: str, username: str, otp_code: str):
    """
    Asynchronously sends a 6-digit verification code email to verify a new email address.
    """
    subject = f"SkillForge — Verify Your New Email Address: {otp_code}"
    message = (
        f"Hi {username},\n\n"
        f"You recently requested to change your SkillForge account email to this address ({new_email}).\n\n"
        f"Your 6-digit confirmation code is: {otp_code}\n\n"
        f"This code will expire in 10 minutes.\n\n"
        f"If you did not request this change, please contact support or secure your account.\n\n"
        f"— The SkillForge Team"
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SkillForge <noreply@skillforge.dev>')

    try:
        logger.info(f"Sending email change OTP to new address {new_email}")
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[new_email],
            fail_silently=False,
        )
        logger.info(f"Email change OTP successfully sent to {new_email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email change OTP to {new_email}: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_email_changed_security_alert_task(self, old_email: str, username: str, new_email: str):
    """
    Security alert sent to the previous email address informing the user that their
    account email was updated.
    """
    subject = "SkillForge Security Alert: Your Account Email Was Changed"
    message = (
        f"Hi {username},\n\n"
        f"This is a security alert to inform you that the email address associated with your SkillForge account was just changed to:\n\n"
        f"  {new_email}\n\n"
        f"If you made this change, no further action is needed.\n\n"
        f"If you did NOT make this change, your account may be compromised. Please contact support immediately at support@skillforge.dev to secure your account.\n\n"
        f"— The SkillForge Security Team"
    )
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SkillForge <noreply@skillforge.dev>')

    try:
        logger.info(f"Sending email change security alert to old address {old_email}")
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[old_email],
            fail_silently=False,
        )
        logger.info(f"Security alert successfully sent to {old_email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send security alert to {old_email}: {exc}")
        raise self.retry(exc=exc)
