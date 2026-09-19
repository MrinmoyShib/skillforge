"""
Public developer portfolio endpoint.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from ..serializers.output import PortfolioDetailOutputSerializer
from ..selectors.portfolio_selectors import get_public_portfolio


class PublicPortfolioAPI(APIView):
    """
    Returns public verified portfolio showcase for any registered developer.
    Accessible without authentication.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Get Developer Public Portfolio",
        description="Public showcase of developer skill ratings, verified projects, track mastery, and achievements.",
        responses={200: PortfolioDetailOutputSerializer}
    )
    def get(self, request, username):
        data = get_public_portfolio(username=username)
        if not data:
            raise NotFound(f"Developer '{username}' not found.")

        serializer = PortfolioDetailOutputSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
