import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
import redis


@pytest.mark.django_db
class TestHealthCheckAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_health_check_success(self):
        response = self.client.get('/api/v1/')
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data['status'] == 'healthy'
        assert data['database'] == 'connected'
        assert data['redis'] == 'connected'
        assert data['version'] == '1.0.0'

    @patch('apps.core.apis.views.redis.from_url')
    def test_health_check_redis_closed_and_timeouts_passed(self, mock_from_url):
        mock_redis = MagicMock()
        mock_from_url.return_value = mock_redis

        response = self.client.get('/api/v1/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['redis'] == 'connected'

        # Verify timeouts were passed
        _, kwargs = mock_from_url.call_args
        assert kwargs.get('socket_connect_timeout') == 2.0
        assert kwargs.get('socket_timeout') == 2.0

        # Verify r.ping() and r.close() were called
        mock_redis.ping.assert_called_once()
        mock_redis.close.assert_called_once()

    @patch('apps.core.apis.views.redis.from_url')
    def test_health_check_redis_failure(self, mock_from_url):
        mock_redis = MagicMock()
        mock_redis.ping.side_effect = redis.ConnectionError("Redis connection refused")
        mock_from_url.return_value = mock_redis

        response = self.client.get('/api/v1/')
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        data = response.data
        assert data['status'] == 'unhealthy'
        assert data['redis'] == 'disconnected'
        assert data['database'] == 'connected'

        # Even on error, close should be called
        mock_redis.close.assert_called_once()

    @patch('django.db.connection.ensure_connection')
    def test_health_check_database_failure(self, mock_ensure_connection):
        mock_ensure_connection.side_effect = Exception("DB unreachable")

        response = self.client.get('/api/v1/')
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        data = response.data
        assert data['status'] == 'unhealthy'
        assert data['database'] == 'disconnected'
