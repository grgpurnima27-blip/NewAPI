from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BookViewSet,
    CategoryViewSet,
    register_view,
    login_view,
    logout_view,
    verify_email,
    password_reset,
    reset_password_page,
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

    # PASSWORD RESET
    path("password-reset/", password_reset),

    # RESET PAGE
    path("reset-password/<uidb64>/<token>/", reset_password_page),
]