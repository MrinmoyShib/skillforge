"""
Admin Analytics & Telemetry API View.
"""
from datetime import timedelta
from django.db import connection
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.accounts.models import User
from apps.problems.models import Problem, TestCase
from apps.projects.models import Project, UserProjectProgress
from apps.submissions.models import Submission, SubmissionStatus
from apps.submissions.engine.judge0 import Judge0Engine
from apps.progress.models import UserProgress
from ..serializers.analytics import AdminAnalyticsOutputSerializer


class AdminAnalyticsAPI(APIView):
    """
    GET /api/v1/admin/analytics/
    Returns platform-wide metrics, activity telemetry, solve distribution, and service health.
    Restricted to staff users (is_staff=True).
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        seven_days_ago = now - timedelta(days=7)

        # Users
        total_users = User.objects.count()
        active_users = User.objects.filter(
            Q(submissions__created_at__gte=seven_days_ago) |
            Q(activities__created_at__gte=seven_days_ago)
        ).distinct().count()
        staff_users = User.objects.filter(is_staff=True).count()

        # Problems & Test Cases
        total_problems = Problem.objects.count()
        published_problems = Problem.objects.filter(is_published=True).count()
        draft_problems = total_problems - published_problems
        total_test_cases = TestCase.objects.count()

        # Projects
        total_projects = Project.objects.count()
        total_milestones_completed = sum(
            r.completed_milestones.count() for r in UserProjectProgress.objects.all()
        )

        # Submissions
        total_submissions = Submission.objects.count()
        accepted_submissions = Submission.objects.filter(status=SubmissionStatus.ACCEPTED).count()
        acceptance_rate = round((accepted_submissions / total_submissions * 100), 1) if total_submissions > 0 else 0.0

        # Solves by Language
        python_solves = UserProgress.objects.filter(solved=True, problem__language='python').count()
        js_solves = UserProgress.objects.filter(solved=True, problem__language='javascript').count()
        cpp_solves = UserProgress.objects.filter(solved=True, problem__language='cpp').count()

        # System Health
        db_status = "healthy"
        try:
            connection.ensure_connection()
        except Exception:
            db_status = "unhealthy"

        judge0 = Judge0Engine()
        sandbox_status = "online (judge0)" if judge0.is_available() else "dev_fallback (isolated python/node/g++)"

        redis_status = "online"
        try:
            import redis
            from django.conf import settings
            r = redis.from_url(settings.CELERY_BROKER_URL)
            r.ping()
        except Exception:
            redis_status = "offline"

        data = {
            "total_users": total_users,
            "active_users": active_users,
            "staff_users": staff_users,
            "total_problems": total_problems,
            "published_problems": published_problems,
            "draft_problems": draft_problems,
            "total_test_cases": total_test_cases,
            "total_projects": total_projects,
            "total_milestones_completed": total_milestones_completed,
            "total_submissions": total_submissions,
            "accepted_submissions": accepted_submissions,
            "acceptance_rate": acceptance_rate,
            "solves_by_language": {
                "python": python_solves,
                "javascript": js_solves,
                "cpp": cpp_solves,
            },
            "system_health": {
                "database": db_status,
                "sandbox": sandbox_status,
                "redis": redis_status,
            }
        }

        serializer = AdminAnalyticsOutputSerializer(data)
        return Response(serializer.data)
