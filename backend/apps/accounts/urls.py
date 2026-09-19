"""
URL routing for SkillForge accounts and authentication endpoints.
"""
from django.urls import path
from .apis.views import (
    CSRFTokenAPI,
    RegisterAPI,
    LoginAPI,
    LogoutAPI,
    CookieTokenRefreshAPI,
    MeAPI,
    ChangePasswordAPI,
    VerifyOTPAPI,
    ResendOTPAPI,
    RequestEmailChangeAPI,
    ConfirmEmailChangeAPI,
)

urlpatterns = [
    path('csrf/', CSRFTokenAPI.as_view(), name='auth-csrf'),
    path('register/', RegisterAPI.as_view(), name='auth-register'),
    path('verify-otp/', VerifyOTPAPI.as_view(), name='auth-verify-otp'),
    path('resend-otp/', ResendOTPAPI.as_view(), name='auth-resend-otp'),
    path('login/', LoginAPI.as_view(), name='auth-login'),
    path('logout/', LogoutAPI.as_view(), name='auth-logout'),
    path('token/refresh/', CookieTokenRefreshAPI.as_view(), name='auth-token-refresh'),
    path('me/', MeAPI.as_view(), name='auth-me'),
    path('change-password/', ChangePasswordAPI.as_view(), name='auth-change-password'),
    path('request-email-change/', RequestEmailChangeAPI.as_view(), name='auth-request-email-change'),
    path('confirm-email-change/', ConfirmEmailChangeAPI.as_view(), name='auth-confirm-email-change'),
]

