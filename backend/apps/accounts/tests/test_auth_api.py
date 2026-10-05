"""
Integration and API tests for accounts & authentication endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.services.auth_services import user_register, user_generate_tokens


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def registered_user(db):
    return user_register(
        username="demodev",
        email="demodev@example.com",
        password="ComplexPassword123!",
        display_name="Demo Dev",
        is_active=True
    )


@pytest.mark.django_db
class TestAuthenticationAPI:
    def test_csrf_handshake(self, api_client):
        url = reverse('auth-csrf')
        response = api_client.get(url)
        assert response.status_code == 200
        assert "csrfToken" in response.data
        assert "csrftoken" in response.cookies

    def test_register_success(self, api_client):
        from apps.accounts.models import EmailVerificationOTP, User
        url = reverse('auth-register')
        payload = {
            "username": "newdev",
            "email": "newdev@example.com",
            "password": "StrongPassword123!",
            "display_name": "New Developer"
        }
        response = api_client.post(url, data=payload, format='json')
        assert response.status_code == 201
        assert response.data["otp_required"] is True
        assert response.data["email"] == "newdev@example.com"

        # Verify user created inactive and OTP was generated
        user = User.objects.get(username="newdev")
        assert not user.is_active
        otp = EmailVerificationOTP.objects.filter(user=user, is_used=False).first()
        assert otp is not None

        # Verify OTP activates user and sets HttpOnly cookies
        otp.set_otp("123456")
        otp.save(update_fields=['otp_code'])
        verify_url = reverse('auth-verify-otp')
        verify_res = api_client.post(verify_url, {"email": "newdev@example.com", "otp_code": "123456"}, format='json')
        assert verify_res.status_code == 200
        user.refresh_from_db()
        assert user.is_active is True
        assert "access_token" in verify_res.cookies
        assert "refresh_token" in verify_res.cookies
        assert verify_res.cookies["access_token"]["httponly"] is True
        assert verify_res.cookies["refresh_token"]["httponly"] is True

    def test_register_duplicate_username(self, api_client, registered_user):
        url = reverse('auth-register')
        payload = {
            "username": "demodev",
            "email": "another@example.com",
            "password": "StrongPassword123!"
        }
        response = api_client.post(url, data=payload, format='json')
        assert response.status_code == 400

    def test_register_duplicate_email(self, api_client, registered_user):
        url = reverse('auth-register')
        payload = {
            "username": "uniqueuser",
            "email": "demodev@example.com",
            "password": "StrongPassword123!"
        }
        response = api_client.post(url, data=payload, format='json')
        assert response.status_code == 400

    def test_register_invalid_username_characters(self):
        from apps.accounts.serializers.input import RegisterInputSerializer
        invalid_usernames = [
            "alex/smith",
            "alex smith",
            "alex@domain.com",
            "alex#dev",
            "alex!cool",
            "alex<script>",
        ]
        for uname in invalid_usernames:
            serializer = RegisterInputSerializer(data={
                "username": uname,
                "email": "test@example.com",
                "password": "StrongPassword123!"
            })
            assert not serializer.is_valid()
            assert "username" in serializer.errors
            assert "letters, numbers, underscores" in str(serializer.errors["username"])

    def test_register_valid_username_with_hyphen_and_underscore(self):
        from apps.accounts.serializers.input import RegisterInputSerializer
        serializer = RegisterInputSerializer(data={
            "username": "alex-smith_99",
            "email": "alex99@example.com",
            "password": "StrongPassword123!"
        })
        assert serializer.is_valid(), serializer.errors

    def test_update_profile_invalid_username(self):
        from apps.accounts.serializers.input import ProfileUpdateInputSerializer
        serializer = ProfileUpdateInputSerializer(data={"username": "bad/username"})
        assert not serializer.is_valid()
        assert "username" in serializer.errors
        assert "letters, numbers, underscores" in str(serializer.errors["username"])

    def test_login_success(self, api_client, registered_user):
        url = reverse('auth-login')
        payload = {
            "username": "demodev",
            "password": "ComplexPassword123!"
        }
        response = api_client.post(url, data=payload, format='json')
        assert response.status_code == 200
        assert response.data["user"]["username"] == "demodev"
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies

    def test_login_invalid_password(self, api_client, registered_user):
        url = reverse('auth-login')
        payload = {
            "username": "demodev",
            "password": "WrongPassword123"
        }
        response = api_client.post(url, data=payload, format='json')
        assert response.status_code == 401
        assert response.data["code"] == "authentication_failed"

    def test_logout(self, api_client, registered_user):
        from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
        access_token, refresh_token = user_generate_tokens(user=registered_user)
        api_client.cookies["access_token"] = access_token
        api_client.cookies["refresh_token"] = refresh_token

        url = reverse('auth-logout')
        response = api_client.post(url)
        assert response.status_code == 200

        # Cookies should be expired/deleted with scoped path
        assert response.cookies["access_token"].value == ""
        assert response.cookies["refresh_token"].value == ""
        assert response.cookies["refresh_token"]["path"] == "/api/v1/auth/"

        # Refresh token must be blacklisted in database
        assert BlacklistedToken.objects.filter(token__token=refresh_token).exists()

        # Subsequent attempt to refresh using blacklisted token must fail with 401
        api_client.cookies["refresh_token"] = refresh_token
        refresh_response = api_client.post(reverse('auth-token-refresh'))
        assert refresh_response.status_code == 401

    def test_logout_fallback_blacklists_user_outstanding_tokens(self, api_client, registered_user):
        from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
        access_token, refresh_token = user_generate_tokens(user=registered_user)
        api_client.cookies["access_token"] = access_token
        # refresh_token cookie is omitted to test fallback blacklisting of authenticated user's tokens

        url = reverse('auth-logout')
        response = api_client.post(url)
        assert response.status_code == 200

        # User's outstanding tokens should be blacklisted via fallback
        assert BlacklistedToken.objects.filter(token__token=refresh_token).exists()

    def test_me_endpoint_authenticated(self, api_client, registered_user):
        access_token, _ = user_generate_tokens(user=registered_user)
        api_client.cookies["access_token"] = access_token

        url = reverse('auth-me')
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["username"] == "demodev"
        assert response.data["profile"]["current_level"] == 1

    def test_me_endpoint_unauthenticated(self, api_client):
        url = reverse('auth-me')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_me_endpoint_patch_profile(self, api_client, registered_user):
        access_token, _ = user_generate_tokens(user=registered_user)
        api_client.cookies["access_token"] = access_token

        url = reverse('auth-me')
        payload = {
            "bio": "Full stack engineer building with Django & React",
            "location": "Tokyo, Japan"
        }
        response = api_client.patch(url, data=payload, format='json')
        assert response.status_code == 200
        assert response.data["profile"]["bio"] == "Full stack engineer building with Django & React"
        assert response.data["profile"]["location"] == "Tokyo, Japan"

    def test_cookie_token_refresh(self, api_client, registered_user):
        _, refresh_token = user_generate_tokens(user=registered_user)
        api_client.cookies["refresh_token"] = refresh_token

        url = reverse('auth-token-refresh')
        response = api_client.post(url)
        assert response.status_code == 200
        assert "access_token" in response.cookies

    def test_me_endpoint_patch_full_profile(self, api_client, registered_user):
        access_token, _ = user_generate_tokens(user=registered_user)
        api_client.cookies["access_token"] = access_token

        url = reverse('auth-me')
        payload = {
            "username": "updateddev",
            "display_name": "Updated Dev",
            "phone_number": "+1 555-0199",
            "bio": "Senior Backend Architect",
            "location": "San Francisco, CA",
            "github_url": "https://github.com/updateddev",
            "linkedin_url": "https://linkedin.com/in/updateddev",
            "twitter_url": "https://x.com/updateddev",
            "website_url": "https://updateddev.io",
        }
        response = api_client.patch(url, data=payload, format='json')
        assert response.status_code == 200
        data = response.data
        assert data["username"] == "updateddev"
        assert data["profile"]["display_name"] == "Updated Dev"
        assert data["profile"]["phone_number"] == "+1 555-0199"
        assert data["profile"]["github_url"] == "https://github.com/updateddev"

    def test_change_password_success(self, api_client, registered_user):
        access_token, _ = user_generate_tokens(user=registered_user)
        api_client.cookies["access_token"] = access_token

        url = reverse('auth-change-password')
        payload = {
            "current_password": "ComplexPassword123!",
            "new_password": "BrandNewPassword999!",
            "confirm_password": "BrandNewPassword999!",
        }
        response = api_client.post(url, data=payload, format='json')
        assert response.status_code == 200
        assert "access_token" in response.cookies

        # Verify new password authenticates
        registered_user.refresh_from_db()
        assert registered_user.check_password("BrandNewPassword999!")

    def test_change_password_wrong_current(self, api_client, registered_user):
        access_token, _ = user_generate_tokens(user=registered_user)
        api_client.cookies["access_token"] = access_token

        url = reverse('auth-change-password')
        payload = {
            "current_password": "IncorrectPassword123!",
            "new_password": "BrandNewPassword999!",
            "confirm_password": "BrandNewPassword999!",
        }
        response = api_client.post(url, data=payload, format='json')
        assert response.status_code == 400
        assert "detail" in response.data

    def test_verify_otp_bypass_prevented_for_active_user(self, api_client, registered_user):
        """
        Verify that an attacker cannot supply a dummy OTP for an already active user
        to bypass password authentication (BUG-005).
        """
        verify_url = reverse('auth-verify-otp')
        payload = {
            "email": registered_user.email,
            "otp_code": "000000"
        }
        response = api_client.post(verify_url, payload, format='json')
        assert response.status_code == 400
        assert "Account is already verified" in str(response.data)
        # Ensure auth cookies were NOT issued
        assert "access_token" not in response.cookies
        assert "refresh_token" not in response.cookies


