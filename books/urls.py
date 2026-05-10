# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import BookViewSet, CategoryViewSet
# from . import views

# router = DefaultRouter()
# router.register(r'books', BookViewSet)
# router.register(r'categories', CategoryViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('reset-password/<str:token>/', views.reset_password_page),
# ]
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from books.views import (
    register_view,
    logout_view,
    verify_email,
    BookViewSet,
    CategoryViewSet
)

from rest_framework.routers import DefaultRouter


# =========================
# SWAGGER CONFIG
# =========================
schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version='v1',
        description="API documentation for Book project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# =========================
# ROUTER (VIEWSETS)
# =========================
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)


# =========================
# URL PATTERNS
# =========================
urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH
    path('api/register/', register_view, name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout/', logout_view, name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # EMAIL VERIFICATION
    path('api/verify-email/<uidb64>/<token>/', verify_email, name='verify-email'),

    # BOOK + CATEGORY API (VIEWSETS)
    path('api/', include(router.urls)),

    # PASSWORD RESET
    path(
        'api/password_reset/',
        include('django_rest_passwordreset.urls', namespace='password_reset')
    ),

    # SWAGGER / REDOC
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]