"""
API views for reading user progress and solved challenge identifiers.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from ..selectors.progress_selectors import (
    get_user_progress_summary,
    get_user_solved_problem_ids,
)
from ..serializers.output import (
    UserProgressSummaryOutputSerializer,
    UserSolvedProblemsOutputSerializer,
)


class UserProgressSummaryAPI(APIView):
    """
    Returns authenticated user's XP, level tier, next level threshold, and daily streak.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get User Progress Summary",
        description="Returns total XP, current level title, streak, and progress percentage to next level.",
        responses={200: UserProgressSummaryOutputSerializer}
    )
    def get(self, request):
        summary = get_user_progress_summary(request.user)
        serializer = UserProgressSummaryOutputSerializer(summary)
        return Response(serializer.data)


class UserSolvedProblemsAPI(APIView):
    """
    Returns list of problem IDs that the authenticated user has successfully solved.
    Used by the frontend to render 'Solved' indicators on challenge cards.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Solved Problem IDs",
        description="Returns array of problem IDs solved by the current user.",
        responses={200: UserSolvedProblemsOutputSerializer}
    )
    def get(self, request):
        solved_ids = get_user_solved_problem_ids(request.user)
        payload = {
            "solved_problem_ids": solved_ids,
            "total_solved": len(solved_ids)
        }
        serializer = UserSolvedProblemsOutputSerializer(payload)
        return Response(serializer.data)

