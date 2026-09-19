"""
API endpoints for listing achievements and user progress.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from ..selectors.achievement_selectors import get_user_achievements_with_status
from ..serializers.output import AchievementOutputSerializer


class AchievementListAPI(APIView):
    """
    Returns full list of platform achievements with unlock status and progress for the current user.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List Achievements",
        description="Returns all platform badges annotated with user unlock status and progress percentage.",
        responses={200: AchievementOutputSerializer(many=True)}
    )
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        achievements = get_user_achievements_with_status(user)
        serializer = AchievementOutputSerializer(achievements, many=True)
        return Response(serializer.data)

