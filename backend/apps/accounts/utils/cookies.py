"""
Cookie management utilities for JWT authentication in SkillForge.
"""
from django.conf import settings
from rest_framework.response import Response


def set_auth_cookies(response: Response, access_token: str, refresh_token: str = None) -> Response:
    """
    Sets access and refresh tokens in HttpOnly cookies on the DRF Response.
    """
    jwt_conf = settings.SIMPLE_JWT

    # Access Token Cookie
    response.set_cookie(
        key=jwt_conf.get('AUTH_COOKIE', 'access_token'),
        value=access_token,
        max_age=int(jwt_conf['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        httponly=jwt_conf.get('AUTH_COOKIE_HTTP_ONLY', True),
        secure=jwt_conf.get('AUTH_COOKIE_SECURE', False),
        samesite=jwt_conf.get('AUTH_COOKIE_SAMESITE', 'Lax'),
        path=jwt_conf.get('AUTH_COOKIE_PATH', '/'),
        domain=jwt_conf.get('AUTH_COOKIE_DOMAIN', None),
    )

    # Refresh Token Cookie (if generated/rotated)
    if refresh_token:
        response.set_cookie(
            key=jwt_conf.get('REFRESH_COOKIE', 'refresh_token'),
            value=refresh_token,
            max_age=int(jwt_conf['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            httponly=jwt_conf.get('AUTH_COOKIE_HTTP_ONLY', True),
            secure=jwt_conf.get('AUTH_COOKIE_SECURE', False),
            samesite=jwt_conf.get('AUTH_COOKIE_SAMESITE', 'Lax'),
            path=jwt_conf.get('REFRESH_COOKIE_PATH', '/api/v1/auth/token/refresh/'),
            domain=jwt_conf.get('AUTH_COOKIE_DOMAIN', None),
        )
    return response


def clear_auth_cookies(response: Response) -> Response:
    """
    Clears both access and refresh cookies from the browser.
    """
    jwt_conf = settings.SIMPLE_JWT
    response.delete_cookie(
        key=jwt_conf.get('AUTH_COOKIE', 'access_token'),
        path=jwt_conf.get('AUTH_COOKIE_PATH', '/'),
        domain=jwt_conf.get('AUTH_COOKIE_DOMAIN', None),
        samesite=jwt_conf.get('AUTH_COOKIE_SAMESITE', 'Lax'),
    )
    response.delete_cookie(
        key=jwt_conf.get('REFRESH_COOKIE', 'refresh_token'),
        path=jwt_conf.get('REFRESH_COOKIE_PATH', '/api/v1/auth/token/refresh/'),
        domain=jwt_conf.get('AUTH_COOKIE_DOMAIN', None),
        samesite=jwt_conf.get('AUTH_COOKIE_SAMESITE', 'Lax'),
    )
    return response

