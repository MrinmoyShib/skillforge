"""
Aggregated Dashboard API view.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from ..selectors.dashboard_selectors import get_aggregated_dashboard_data
from ..serializers.output import DashboardDataOutputSerializer


class DashboardAPI(APIView):
    """
    Returns aggregated metrics, category mastery, recommended problems, and recent submissions.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Dashboard Data",
        description="Unified endpoint delivering user progression stats, category mastery bars, recommendations, and recent submissions.",
        responses={200: DashboardDataOutputSerializer}
    )
    def get(self, request):
        dashboard_data = get_aggregated_dashboard_data(request.user)
        serializer = DashboardDataOutputSerializer(dashboard_data)
        return Response(serializer.data)

