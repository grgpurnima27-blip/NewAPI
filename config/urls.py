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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from books.views import verify_email, reset_password_page
from django_rest_passwordreset.views import ResetPasswordConfirm

schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # EMAIL VERIFY
    path('api/verify-email/<uidb64>/<token>/', verify_email),

    # PASSWORD RESET
    path('api/password_reset/', include('django_rest_passwordreset.urls')),
    path('api/password_reset/confirm/', ResetPasswordConfirm.as_view()),

    # RESET PAGE
    path('reset-password/<str:token>/', reset_password_page),

    # APP
    path('api/', include('books.urls')),

    # SWAGGER
    path('swagger/', schema_view.with_ui('swagger')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)