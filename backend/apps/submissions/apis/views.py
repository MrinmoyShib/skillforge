"""
API views for creating, listing, and polling code submissions.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from apps.core.pagination import StandardPagination
from ..serializers.input import (
    SubmissionCreateInputSerializer,
    SubmissionFilterInputSerializer,
)
from ..serializers.output import (
    SubmissionListOutputSerializer,
    SubmissionDetailOutputSerializer,
)
from ..selectors.submission_selectors import (
    submission_list_for_user,
    submission_get_by_id,
)
from ..services.submission_services import submission_create


class SubmissionListCreateAPI(APIView):
    """
    POST: Submit code for evaluation (runs asynchronous Celery sandbox task).
    GET: List authenticated user's submission history.
    """
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    @extend_schema(
        summary="Create Submission",
        description="Submits source code for evaluation against test cases. Returns immediately with PENDING status.",
        request=SubmissionCreateInputSerializer,
        responses={201: SubmissionDetailOutputSerializer}
    )
    def post(self, request):
        serializer = SubmissionCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission = submission_create(user=request.user, **serializer.validated_data)
        output_serializer = SubmissionDetailOutputSerializer(submission, context={'request': request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="List Submissions",
        description="Returns the authenticated user's submissions history, optionally filtered by problem ID.",
        parameters=[SubmissionFilterInputSerializer],
        responses={200: SubmissionListOutputSerializer(many=True)}
    )
    def get(self, request):
        filter_serializer = SubmissionFilterInputSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        submissions = submission_list_for_user(user=request.user, filters=filter_serializer.validated_data)
        paginator = self.pagination_class()
        paginated_submissions = paginator.paginate_queryset(submissions, request)
        serializer = SubmissionListOutputSerializer(paginated_submissions, many=True)
        return paginator.get_paginated_response(serializer.data)


class SubmissionDetailAPI(APIView):
    """
    Retrieves the status, verdict, execution stats, and sanitized test-case outcomes of a submission.
    Frontend polls this endpoint until status is terminal.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Submission Details",
        description="Fetches a submission by ID. Includes sanitized per-test-case results.",
        responses={200: SubmissionDetailOutputSerializer}
    )
    def get(self, request, submission_id):
        submission = submission_get_by_id(submission_id=submission_id, user=request.user)
        if not submission:
            raise NotFound("Submission not found.")

        serializer = SubmissionDetailOutputSerializer(submission, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

