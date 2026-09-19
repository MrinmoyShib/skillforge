"""
API Views for SkillForge Authentication & Accounts.
"""
from django.conf import settings
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema

from ..serializers.input import (
    RegisterInputSerializer,
    LoginInputSerializer,
    CookieTokenRefreshSerializer,
    ProfileUpdateInputSerializer,
    ChangePasswordInputSerializer,
)
from ..serializers.output import (
    UserOutputSerializer,
    AuthMessageOutputSerializer,
    CSRFOutputSerializer,
)
from ..services.auth_services import (
    user_register,
    user_authenticate,
    user_generate_tokens,
    user_profile_update,
    user_change_password,
    token_blacklist_refresh,
)
from ..selectors.user_selectors import user_get_by_id
from ..utils.cookies import set_auth_cookies, clear_auth_cookies


class CSRFTokenAPI(APIView):
    """
    Sets the 'csrftoken' cookie and returns the token in response JSON.
    Frontend calls this on initial application bootstrap.
    """
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    @extend_schema(
        summary="CSRF Handshake",
        description="Sets the csrftoken cookie and returns the token for SPA state.",
        responses={200: CSRFOutputSerializer}
    )
    def get(self, request):
        token = get_token(request)
        return Response({
            "detail": "CSRF cookie set.",
            "csrfToken": token
        }, status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    """
    Creates a new user account, initializes profile, and sets JWT cookies.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Registration",
        description="Registers a new user and sets authentication cookies.",
        request=RegisterInputSerializer,
        responses={201: AuthMessageOutputSerializer}
    )
    def post(self, request):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_register(**serializer.validated_data)
        access_token, refresh_token = user_generate_tokens(user=user)

        user_data = UserOutputSerializer(user_get_by_id(user_id=user.id)).data
        response = Response({
            "detail": "Registration successful.",
            "user": user_data
        }, status=status.HTTP_201_CREATED)

        return set_auth_cookies(response, access_token=access_token, refresh_token=refresh_token)


class LoginAPI(APIView):
    """
    Authenticates user credentials and issues HttpOnly JWT cookies.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Login",
        description="Authenticates username/email and password, then sets JWT cookies.",
        request=LoginInputSerializer,
        responses={200: AuthMessageOutputSerializer}
    )
    def post(self, request):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_authenticate(**serializer.validated_data)
        if not user:
            return Response(
                {"detail": "Invalid credentials.", "code": "authentication_failed"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token, refresh_token = user_generate_tokens(user=user)
        user_data = UserOutputSerializer(user_get_by_id(user_id=user.id)).data

        response = Response({
            "detail": "Login successful.",
            "user": user_data
        }, status=status.HTTP_200_OK)

        return set_auth_cookies(response, access_token=access_token, refresh_token=refresh_token)


class LogoutAPI(APIView):
    """
    Invalidates the active refresh token and clears all authentication cookies.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="User Logout",
        description="Blacklists current refresh token and clears authentication cookies.",
        responses={200: AuthMessageOutputSerializer}
    )
    def post(self, request):
        refresh_cookie_name = settings.SIMPLE_JWT.get('REFRESH_COOKIE', 'refresh_token')
        raw_refresh_token = request.COOKIES.get(refresh_cookie_name) or request.data.get('refresh')

        if raw_refresh_token:
            token_blacklist_refresh(refresh_token_str=raw_refresh_token)

        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        return clear_auth_cookies(response)


class CookieTokenRefreshAPI(TokenRefreshView):
    """
    Silent token refresh: reads refresh token from HttpOnly cookie,
    rotates it, blacklists the old token, and sets new cookies.
    """
    serializer_class = CookieTokenRefreshSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Token Refresh",
        description="Refreshes the access token using the HttpOnly refresh token cookie.",
        responses={200: AuthMessageOutputSerializer}
    )
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            if access_token:
                set_auth_cookies(response, access_token=access_token, refresh_token=refresh_token)
                response.data = {"detail": "Token successfully refreshed."}
        return super().finalize_response(request, response, *args, **kwargs)


class MeAPI(APIView):
    """
    Current authenticated user endpoint.
    GET: Returns user info and profile.
    PATCH: Updates profile fields.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get Current User",
        description="Returns the authenticated user details and profile stats.",
        responses={200: UserOutputSerializer}
    )
    def get(self, request):
        user = user_get_by_id(user_id=request.user.id)
        serializer = UserOutputSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update Profile",
        description="Updates profile and user fields for the authenticated user.",
        request=ProfileUpdateInputSerializer,
        responses={200: UserOutputSerializer}
    )
    def patch(self, request):
        serializer = ProfileUpdateInputSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user_profile_update(user=request.user, **serializer.validated_data)
        user = user_get_by_id(user_id=request.user.id)
        return Response(UserOutputSerializer(user).data, status=status.HTTP_200_OK)


class ChangePasswordAPI(APIView):
    """
    Allows an authenticated user to change their account password securely.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Change Password",
        description="Validates current password and updates to a new password.",
        request=ChangePasswordInputSerializer,
        responses={200: AuthMessageOutputSerializer}
    )
    def post(self, request):
        serializer = ChangePasswordInputSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user_change_password(user=request.user, new_password=serializer.validated_data['new_password'])

        # Generate fresh tokens so user stays seamlessly logged in
        access_token, refresh_token = user_generate_tokens(user=request.user)

        response = Response({
            "detail": "Password changed successfully."
        }, status=status.HTTP_200_OK)

        return set_auth_cookies(response, access_token=access_token, refresh_token=refresh_token)

