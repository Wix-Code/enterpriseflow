from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


def generate_tokens(user):
    """
    Generate access and refresh tokens for a user.
    """

    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def send_password_reset_email(user):
    """
    Generate a password reset link and send it to the user.
    """

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = default_token_generator.make_token(user)

    frontend_url = getattr(
        settings,
        "FRONTEND_URL",
        "http://localhost:3000",
    )

    reset_link = (
        f"{frontend_url}/reset-password/"
        f"?uid={uid}&token={token}"
    )

    send_mail(
        subject="Reset your EnterpriseFlow password",
        message=(
            f"Hello {user.first_name or 'there'},\n\n"
            "You requested a password reset.\n\n"
            f"Use this link to reset your password:\n{reset_link}\n\n"
            "If you did not request this, ignore this email."
        ),
        from_email=getattr(
            settings,
            "DEFAULT_FROM_EMAIL",
            None,
        ),
        recipient_list=[user.email],
        fail_silently=False,
    )