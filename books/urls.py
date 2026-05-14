from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BookViewSet,
    CategoryViewSet,
    register_view,
    login_view,
    logout_view,
    verify_email,
    reset_password_page,
    password_reset_confirm,
    profile_view,
    profile_update,
)

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

    # FIXED RESET PASSWORD PAGE ROUTE
    path("reset-password/<uidb64>/<token>/", reset_password_page),

    # RESET CONFIRM API
    path("api/password-reset/confirm/", password_reset_confirm),

    # PROFILE
    path("profile/", profile_view),
    path("profile/update/", profile_update),
]