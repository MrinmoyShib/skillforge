from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck
from rest_framework_simplejwt.authentication import JWTAuthentication


def dummy_get_response(request):
    return None


def enforce_csrf(request):
    """
    Manually enforces Django's CSRF check on API views that authenticate via cookies.
    """
    check = CSRFCheck(dummy_get_response)
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied(f"CSRF Failed: {reason}")


class JWTCookieAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication backend reading from Authorization headers
    with fallback to HttpOnly cookies.
    """
    def authenticate(self, request):
        header = self.get_header(request)

        # 1. Header-based authentication (Bearer token)
        if header is not None:
            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token

        # 2. Cookie-based authentication fallback
        cookie_name = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token')
        raw_token = request.COOKIES.get(cookie_name)

        if raw_token is None:
            return None

        # CRITICAL: If credentials arrived via cookies, enforce CSRF
        enforce_csrf(request)

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

