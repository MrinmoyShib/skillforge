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
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

User = get_user_model()

from ..serializers.input import (
    RegisterInputSerializer,
    LoginInputSerializer,
    CookieTokenRefreshSerializer,
    ProfileUpdateInputSerializer,
    ChangePasswordInputSerializer,
    VerifyOTPInputSerializer,
    ResendOTPInputSerializer,
    RequestEmailChangeInputSerializer,
    ConfirmEmailChangeInputSerializer,
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
    user_verify_otp,
    user_resend_otp,
    user_request_email_change,
    user_confirm_email_change,
)
from ..selectors.user_selectors import user_get_by_id
from ..utils.cookies import set_auth_cookies, clear_auth_cookies


from rest_framework.throttling import ScopedRateThrottle

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
    Creates a new inactive user account and sends a 6-digit email verification OTP.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="User Registration",
        description="Registers a new user account and sends an email verification OTP code.",
        request=RegisterInputSerializer,
        responses={201: inline_serializer(
            name="RegisterResponse",
            fields={
                "detail": serializers.CharField(),
                "email": serializers.EmailField(),
                "otp_required": serializers.BooleanField(),
            }
        )}
    )
    def post(self, request):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_register(**serializer.validated_data)

        return Response({
            "detail": "Verification code sent to your email.",
            "email": user.email,
            "otp_required": True,
        }, status=status.HTTP_201_CREATED)


class VerifyOTPAPI(APIView):
    """
    Verifies the 6-digit OTP code, activates the user account, and issues JWT cookies.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="Verify Email OTP",
        description="Verifies the 6-digit OTP code, activates the user, and sets authentication cookies.",
        request=VerifyOTPInputSerializer,
        responses={200: AuthMessageOutputSerializer}
    )
    def post(self, request):
        serializer = VerifyOTPInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_verify_otp(**serializer.validated_data)
        access_token, refresh_token = user_generate_tokens(user=user)

        user_data = UserOutputSerializer(user_get_by_id(user_id=user.id)).data
        response = Response({
            "detail": "Email verified successfully.",
            "user": user_data
        }, status=status.HTTP_200_OK)

        return set_auth_cookies(response, access_token=access_token, refresh_token=refresh_token)


class ResendOTPAPI(APIView):
    """
    Resends a new 6-digit OTP to the user's email with a 60-second cooldown.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="Resend Verification OTP",
        description="Generates and emails a new OTP code if 60 seconds have passed since the previous request.",
        request=ResendOTPInputSerializer,
        responses={200: inline_serializer(
            name="ResendOTPResponse",
            fields={"detail": serializers.CharField()}
        )}
    )
    def post(self, request):
        serializer = ResendOTPInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_resend_otp(**serializer.validated_data)

        return Response({
            "detail": "A new verification code has been sent to your email."
        }, status=status.HTTP_200_OK)


class LoginAPI(APIView):
    """
    Authenticates user credentials and issues HttpOnly JWT cookies.
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

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
            # Check if user exists but is inactive (unverified email)
            username_or_email = serializer.validated_data.get('username')
            unverified_user = None
            if '@' in username_or_email:
                unverified_user = User.objects.filter(email__iexact=username_or_email, is_active=False).first()
            else:
                unverified_user = User.objects.filter(username__iexact=username_or_email, is_active=False).first()

            if unverified_user and unverified_user.check_password(serializer.validated_data.get('password')):
                return Response(
                    {
                        "detail": "Email not verified. Please verify your email with the verification code.",
                        "email": unverified_user.email,
                        "otp_required": True,
                        "code": "email_not_verified"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

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


class RequestEmailChangeAPI(APIView):
    """
    Initiates an email address change. Requires current password for re-authentication
    and sends a 6-digit OTP code to the requested new email address.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="Request Email Change",
        description="Validates current password and sends a 6-digit OTP to the new email address.",
        request=RequestEmailChangeInputSerializer,
        responses={200: inline_serializer(
            name="RequestEmailChangeResponse",
            fields={
                "detail": serializers.CharField(),
                "new_email": serializers.EmailField(),
            }
        )}
    )
    def post(self, request):
        serializer = RequestEmailChangeInputSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user_request_email_change(
            user=request.user,
            new_email=serializer.validated_data['new_email'],
            current_password=serializer.validated_data['current_password']
        )

        return Response({
            "detail": "Verification code sent to your new email address.",
            "new_email": serializer.validated_data['new_email'],
        }, status=status.HTTP_200_OK)


class ConfirmEmailChangeAPI(APIView):
    """
    Finalizes the email address change by verifying the 6-digit OTP sent to the new address.
    Dispatches a security alert notification to the previous email address.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    @extend_schema(
        summary="Confirm Email Change",
        description="Verifies the OTP code sent to the new email address and updates the account.",
        request=ConfirmEmailChangeInputSerializer,
        responses={200: inline_serializer(
            name="ConfirmEmailChangeResponse",
            fields={
                "detail": serializers.CharField(),
                "email": serializers.EmailField(),
            }
        )}
    )
    def post(self, request):
        serializer = ConfirmEmailChangeInputSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user, old_email = user_confirm_email_change(
            user=request.user,
            new_email=serializer.validated_data['new_email'],
            otp_code=serializer.validated_data['otp']
        )

        return Response({
            "detail": "Email address updated successfully.",
            "email": user.email,
        }, status=status.HTTP_200_OK)

