"""
Admin Submissions ViewSet with Code Inspector and Re-Judge Engine.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.submissions.models import Submission
from apps.submissions.tasks import evaluate_submission_task
from ..serializers.submissions import (
    AdminSubmissionListSerializer,
    AdminSubmissionDetailSerializer,
)


class AdminSubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for inspecting platform submissions and triggering re-judging.
    """
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = Submission.objects.select_related('user', 'problem').prefetch_related(
            'results__test_case'
        )

        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        language = self.request.query_params.get('language')
        if language:
            qs = qs.filter(language=language)

        username = self.request.query_params.get('username')
        if username:
            qs = qs.filter(user__username__icontains=username)

        problem_slug = self.request.query_params.get('problem_slug')
        if problem_slug:
            qs = qs.filter(problem__slug=problem_slug)

        return qs.order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminSubmissionListSerializer
        return AdminSubmissionDetailSerializer

    @action(detail=True, methods=['post'], url_path='rejudge')
    def rejudge(self, request, pk=None):
        """
        POST /api/v1/admin/submissions/<id>/rejudge/
        Re-evaluates the submission against the problem's test cases.
        """
        submission = self.get_object()
        
        # Execute evaluation task synchronously or in background
        # Since admin is waiting for immediate feedback in the studio, execute synchronously
        evaluate_submission_task(submission.id)

        # Refresh from database
        submission.refresh_from_db()
        serializer = AdminSubmissionDetailSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)

