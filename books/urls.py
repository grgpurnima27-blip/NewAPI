from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [

    path("", include(router.urls)),

    # AUTH
    path("register/", views.register_view),
    path("login/", views.login_view),
    path("logout/", views.logout_view),

    # EMAIL VERIFY
    path("verify-email/<uidb64>/<token>/", views.verify_email),

    # PASSWORD RESET
    path("forgot-password/", views.forgot_password),
    path("reset-password/<uidb64>/<token>/", views.reset_password_page),
    path("password-reset/confirm/", views.password_reset_confirm),

    # PROFILE
    path("profile/", views.profile_view),
    path("profile/update/", views.profile_update),
]