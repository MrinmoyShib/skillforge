"""
REST API endpoints for Guided Projects and Milestone Verification.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from drf_spectacular.utils import extend_schema

from ..models import Project, ProjectMilestone
from ..serializers.input import ProjectFilterInputSerializer, MilestoneVerifyInputSerializer
from ..serializers.output import (
    ProjectListOutputSerializer,
    ProjectDetailOutputSerializer,
    UserProjectProgressOutputSerializer,
    MilestoneVerificationResultSerializer,
)
from ..selectors.project_selectors import project_list, project_get_by_slug
from ..services.project_services import start_project, verify_milestone


class ProjectListAPI(APIView):
    """
    Lists published guided engineering projects with optional track and difficulty filtering.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List Guided Projects",
        parameters=[ProjectFilterInputSerializer],
        responses={200: ProjectListOutputSerializer(many=True)}
    )
    def get(self, request):
        filter_serializer = ProjectFilterInputSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        user = request.user if request.user.is_authenticated else None
        projects = project_list(user=user, filters=filter_serializer.validated_data)
        serializer = ProjectListOutputSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectDetailAPI(APIView):
    """
    Retrieves full guided project specifications, milestone sequence, and user progress.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get Guided Project Detail",
        responses={200: ProjectDetailOutputSerializer}
    )
    def get(self, request, slug):
        user = request.user if request.user.is_authenticated else None
        project_data = project_get_by_slug(slug=slug, user=user)
        if not project_data:
            raise NotFound("Guided project not found.")

        serializer = ProjectDetailOutputSerializer(project_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectStartAPI(APIView):
    """
    Initializes student enrollment for a guided project lab.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Start Guided Project Lab",
        responses={200: UserProjectProgressOutputSerializer}
    )
    def post(self, request, slug):
        project = Project.objects.filter(slug=slug, is_published=True).first()
        if not project:
            raise NotFound("Guided project not found.")

        progress = start_project(user=request.user, project=project)
        serializer = UserProjectProgressOutputSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MilestoneVerifyAPI(APIView):
    """
    Evaluates student milestone solution in sandboxed execution engine and awards XP on pass.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Verify Milestone Solution",
        request=MilestoneVerifyInputSerializer,
        responses={200: MilestoneVerificationResultSerializer}
    )
    def post(self, request, slug, milestone_id):
        project = Project.objects.filter(slug=slug, is_published=True).first()
        if not project:
            raise NotFound("Guided project not found.")

        milestone = ProjectMilestone.objects.filter(project=project, id=milestone_id).first()
        if not milestone:
            raise NotFound("Milestone not found for this project.")

        serializer = MilestoneVerifyInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_code = serializer.validated_data['source_code']
        verification_result = verify_milestone(
            user=request.user,
            project=project,
            milestone=milestone,
            source_code=source_code
        )

        output_serializer = MilestoneVerificationResultSerializer(verification_result)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

