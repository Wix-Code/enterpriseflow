from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    RefreshTokenView,
    LogoutView,
    ProfileView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
)


urlpatterns = [
    # Authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # User profile
    path("me/", ProfileView.as_view(), name="profile"),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),

    # Password recovery
    path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot-password",
    ),
    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
]