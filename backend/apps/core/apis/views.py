from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema, inline_serializer
from django.db import connection
from django.conf import settings
import redis


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
                    "redis": serializers.CharField(),
                    "version": serializers.CharField(),
                }
            )
        }
    )
    def get(self, request):
        db_status = "connected"
        overall_status_code = status.HTTP_200_OK
        
        try:
            connection.ensure_connection()
        except Exception:
            db_status = "disconnected"
            overall_status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            
        redis_status = "connected"
        try:
            r = redis.from_url(settings.CELERY_BROKER_URL)
            r.ping()
        except Exception:
            redis_status = "disconnected"
            overall_status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return Response({
            "status": "healthy" if overall_status_code == status.HTTP_200_OK else "unhealthy",
            "database": db_status,
            "redis": redis_status,
            "version": "1.0.0"
        }, status=overall_status_code)
