"""
Celery background tasks for achievements evaluation.
"""
from celery import shared_task
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.achievements.tasks.check_achievements_task', bind=True, max_retries=3)
def check_achievements_task(self, user_id: int):
    """
    Asynchronously evaluates and grants achievements for a given user.
    """
    User = get_user_model()
    user = User.objects.filter(id=user_id).first()
    if not user:
        return
    try:
        from .services.achievement_engine import check_and_grant_achievements
        check_and_grant_achievements(user)
    except Exception as exc:
        logger.warning(f"Error checking achievements asynchronously for user {user_id}: {exc}")
        raise self.retry(exc=exc, countdown=5)

