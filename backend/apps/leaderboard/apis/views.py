"""
API view for querying the global developer leaderboard.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter

from ..selectors.leaderboard_selectors import get_global_leaderboard
from ..serializers.output import LeaderboardResponseSerializer


class LeaderboardAPI(APIView):
    """
    Returns global leaderboard rankings, sorting options, and the authenticated user's current rank.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get Global Leaderboard",
        description="Returns sorted, ranked list of users by XP or solved challenges.",
        parameters=[
            OpenApiParameter(name='sort', type=str, description="Sort criteria: 'xp' (default) or 'solved'", required=False),
            OpenApiParameter(name='limit', type=int, description="Number of results to return (max 100)", required=False),
            OpenApiParameter(name='offset', type=int, description="Pagination offset", required=False),
        ],
        responses={200: LeaderboardResponseSerializer}
    )
    def get(self, request):
        sort_by = request.query_params.get('sort', 'xp')
        try:
            limit = min(100, max(1, int(request.query_params.get('limit', 50))))
        except ValueError:
            limit = 50

        try:
            offset = max(0, int(request.query_params.get('offset', 0)))
        except ValueError:
            offset = 0

        user = request.user if request.user.is_authenticated else None
        leaderboard_data = get_global_leaderboard(
            sort_by=sort_by,
            current_user=user,
            limit=limit,
            offset=offset
        )
        serializer = LeaderboardResponseSerializer(leaderboard_data)
        return Response(serializer.data)

