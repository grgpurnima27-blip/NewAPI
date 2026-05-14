"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from books import views


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="Auth + Books + Email Verification + Reset System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # ADMIN
    path("admin/", admin.site.urls),

    # JWT AUTH
    path("api/login/", TokenObtainPairView.as_view(), name="jwt_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),

    # AUTH (CUSTOM)
    path("api/register/", views.register_view),
    path("api/verify-email/<uidb64>/<token>/", views.verify_email),

    path("api/forgot-password/", views.forgot_password),
    path("api/password-reset/confirm/", views.password_reset_confirm),

    # IMPORTANT: HTML RESET PAGE
    path("reset-password/<uidb64>/<token>/", views.reset_password_page),


    # APP ROUTES
    path("api/", include("books.urls")),


    # SWAGGER
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
]