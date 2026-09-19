from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer
from django.db import connection


class HealthCheckView(APIView):
    """
    Health check endpoint verifying API uptime and PostgreSQL database connectivity.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Health Check",
        description="Returns API status, database connectivity state, and application version.",
        responses={
            200: inline_serializer(
                name="HealthCheckResponse",
                fields={
                    "status": serializers.CharField(),
                    "database": serializers.CharField(),
                    "version": serializers.CharField(),
                }
            )
        }
    )
    def get(self, request):
        db_status = "connected"
        try:
            connection.ensure_connection()
        except Exception:
            db_status = "disconnected"

        return Response({
            "status": "healthy",
            "database": db_status,
            "version": "1.0.0"
        })
