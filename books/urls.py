from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    verify_email,
    reset_password_page,
    password_reset_confirm,
    forgot_password,
    profile_view,
    profile_update,
    BookViewSet,
    CategoryViewSet,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),

    # AUTH
    path("register/", register_view),
    path("login/", login_view),
    path("logout/", logout_view),

    # EMAIL VERIFY
    path("verify-email/<uidb64>/<token>/", verify_email),

    # PASSWORD RESET FLOW
    path("forgot-password/", forgot_password),
    path("reset-password/<uidb64>/<token>/", reset_password_page),
    path("password-reset/confirm/", password_reset_confirm),

    # PROFILE
    path("profile/", profile_view),
    path("profile/update/", profile_update),
]