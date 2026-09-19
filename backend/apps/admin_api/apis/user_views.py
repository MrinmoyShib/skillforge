"""
Admin User Management ViewSet with Student Telemetry and Manual XP Adjustment.
"""
from django.db import transaction
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.accounts.models import User
from apps.progress.models import ActivityLog
from apps.progress.services.leveling import calculate_level
from ..serializers.users import (
    AdminUserListSerializer,
    AdminUserDetailSerializer,
    AdminUserUpdateSerializer,
    AdminAdjustXPInputSerializer,
)


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users, inspecting student telemetry, and adjusting XP.
    """
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'patch', 'post']

    def get_queryset(self):
        qs = User.objects.select_related('profile').annotate(
            problems_solved_count=Count('progress_records', filter=Q(progress_records__solved=True), distinct=True)
        )

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(profile__display_name__icontains=search)
            )

        is_staff = self.request.query_params.get('is_staff')
        if is_staff is not None:
            qs = qs.filter(is_staff=is_staff.lower() in ('true', '1'))

        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() in ('true', '1'))

        return qs.order_by('-date_joined')

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminUserListSerializer
        elif self.action == 'retrieve':
            return AdminUserDetailSerializer
        elif self.action in ('update', 'partial_update'):
            return AdminUserUpdateSerializer
        return AdminUserDetailSerializer

    @action(detail=True, methods=['post'], url_path='adjust-xp')
    def adjust_xp(self, request, pk=None):
        """
        POST /api/v1/admin/users/<id>/adjust-xp/
        Manually adds or deducts XP for a user and re-computes their level atomically.
        Logs an ActivityLog entry for auditing.
        """
        user = self.get_object()
        serializer = AdminAdjustXPInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        xp_delta = serializer.validated_data['xp_delta']
        reason = serializer.validated_data['reason']

        with transaction.atomic():
            profile = user.profile
            new_xp = max(0, profile.total_xp + xp_delta)
            profile.total_xp = new_xp

            lvl_info = calculate_level(new_xp)
            old_level = profile.current_level
            profile.current_level = lvl_info['level']
            profile.save(update_fields=['total_xp', 'current_level', 'updated_at'])

            # Log activity
            action_desc = f"Admin XP Adjustment ({'+' if xp_delta >= 0 else ''}{xp_delta} XP): {reason}"
            ActivityLog.objects.create(
                user=user,
                activity_type=ActivityLog.ActivityType.LEVEL_UP if profile.current_level > old_level else ActivityLog.ActivityType.SUBMISSION,
                description=action_desc,
                metadata={"xp_delta": xp_delta, "reason": reason}
            )

        detail_serializer = AdminUserDetailSerializer(user)
        return Response(detail_serializer.data, status=status.HTTP_200_OK)
