"""
Admin Guided Projects ViewSet with Milestone Management.
"""
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.projects.models import Project, ProjectMilestone
from ..serializers.projects import (
    AdminProjectListSerializer,
    AdminProjectDetailSerializer,
    AdminProjectCreateUpdateSerializer,
    AdminProjectMilestoneSerializer,
)


class AdminProjectViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for Guided Projects in Admin Studio.
    """
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Project.objects.prefetch_related('milestones').annotate(
            milestones_count=Count('milestones', distinct=True)
        ).order_by('order', 'id')

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminProjectListSerializer
        elif self.action == 'retrieve':
            return AdminProjectDetailSerializer
        return AdminProjectCreateUpdateSerializer

    @action(detail=True, methods=['post'], url_path='milestones')
    def add_milestone(self, request, pk=None):
        """
        POST /api/v1/admin/projects/<id>/milestones/
        Adds a new milestone to the guided project.
        """
        project = self.get_object()
        serializer = AdminProjectMilestoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        milestone = ProjectMilestone.objects.create(project=project, **serializer.validated_data)
        return Response(AdminProjectMilestoneSerializer(milestone).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'], url_path=r'milestones/(?P<milestone_id>\d+)')
    def update_milestone(self, request, pk=None, milestone_id=None):
        """
        PUT/PATCH /api/v1/admin/projects/<id>/milestones/<milestone_id>/
        Updates a specific milestone.
        """
        project = self.get_object()
        milestone = get_object_or_404(ProjectMilestone, project=project, id=milestone_id)
        serializer = AdminProjectMilestoneSerializer(milestone, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path=r'milestones/(?P<milestone_id>\d+)')
    def delete_milestone(self, request, pk=None, milestone_id=None):
        """
        DELETE /api/v1/admin/projects/<id>/milestones/<milestone_id>/
        Deletes a specific milestone.
        """
        project = self.get_object()
        milestone = get_object_or_404(ProjectMilestone, project=project, id=milestone_id)
        milestone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

