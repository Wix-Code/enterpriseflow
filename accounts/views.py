from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

from .utils import success_response, error_response

from .services.auth_service import (
    generate_tokens,
    send_password_reset_email,
)


class RegisterView(APIView):
    """
    Register a new EnterpriseFlow user.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        tokens = generate_tokens(user)

        data = {
            "user": UserSerializer(user).data,
            "tokens": tokens,
        }

        return success_response(
            message="Account registered successfully.",
            data=data,
            http_status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    Authenticate a user using email and password.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        tokens = generate_tokens(user)

        return success_response(
            message="Login successful.",
            data={
                "user": UserSerializer(user).data,
                "tokens": tokens,
            },
        )


class RefreshTokenView(APIView):
    """
    Generate a new access token using a refresh token.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = TokenRefreshSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        return success_response(
            message="Token refreshed successfully.",
            data=serializer.validated_data,
        )


class LogoutView(APIView):
    """
    Blacklist a refresh token to log out the user.
    """

    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return error_response(
                message="Refresh token is required.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError:
            return error_response(
                message="Invalid or expired refresh token.",
                http_status=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Logout successful.",
            data=None,
        )


class ProfileView(APIView):
    """
    Retrieve and update the authenticated user's profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return success_response(
            message="Profile retrieved successfully.",
            data=serializer.data,
        )

    def patch(self, request):

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return success_response(
            message="Profile updated successfully.",
            data=serializer.data,
        )


class ChangePasswordView(APIView):
    """
    Change the authenticated user's password.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        user = request.user

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save(update_fields=["password"])

        return success_response(
            message="Password changed successfully. Please sign in again.",
            data=None,
        )


class ForgotPasswordView(APIView):
    """
    Send a password reset email.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].strip()

        user = User.objects.filter(
            email__iexact=email
        ).first()

        if user and user.is_active:
            send_password_reset_email(user)

        # Do not reveal whether an email belongs to an account.
        return success_response(
            message=(
                "If an account exists with that email, "
                "password reset instructions have been sent."
            ),
            data=None,
        )


class ResetPasswordView(APIView):
    """
    Set a new password using a valid reset token.
    """

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        user.set_password(
            serializer.validated_data["new_password"]
        )

        user.save(update_fields=["password"])

        return success_response(
            message="Password reset successfully. You can now sign in.",
            data=None,
        )