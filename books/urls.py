from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    register_view,
    login_view,
    logout_view,
    verify_email,
    forgot_password,
    reset_password_page,
    password_reset_confirm,
    profile_update,
    BookViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [

    # BOOKS + CATEGORIES
    path("", include(router.urls)),

    # AUTH
    path("register/", register_view),
    path("login/", login_view),
    path("logout/", logout_view),

    # EMAIL VERIFICATION
    path(
        "verify-email/<uidb64>/<token>/",
        verify_email
    ),

    # PASSWORD RESET
    path("forgot-password/", forgot_password),

    path(
        "reset-password/<uidb64>/<token>/",
        reset_password_page
    ),

    path(
        "password-reset-confirm/",
        password_reset_confirm
    ),

    # PROFILE
    path("profile/update/", profile_update),
]