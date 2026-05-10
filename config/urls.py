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
# from django.contrib import admin
# from django.urls import path, include
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView, TokenRefreshView,
# )
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi


# schema_view= get_schema_view(
#     openapi.Info(
#         title="Book API",
#         default_version='v1',
#         description="API documentation for Book project",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# from django.contrib import admin
# from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from books.views import register_view, logout_view  # ✅ Add this import

# urlpatterns = [
#     path('admin/', admin.site.urls),

#     #  Register (Sign Up)
#     path('api/register/', register_view, name='register'),

#     #  Login (Sign In)
#     path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

#     #  Logout (Sign Out)
#     path('api/logout/', logout_view, name='logout'),

#     # Token refresh (keep this)
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

#     path('', include('books.urls')),
#     path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

#     # Swagger URLs
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
# ]

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from books.views import register_view, logout_view
from books.views import verify_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version='v1',
        description="API documentation for Book project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)


# TEMPORARY - DELETE AFTER CREATING SUPERUSER
@csrf_exempt
def create_superuser(request):
    if request.method == 'POST':
        from django.contrib.auth.models import User
        data = json.loads(request.body)
        if not User.objects.filter(username=data['username']).exists():
            User.objects.create_superuser(
                username=data['username'],
                password=data['password'],
                email=data.get('email', '')
            )
            return JsonResponse({'message': 'Superuser created!'})
        return JsonResponse({'message': 'User already exists!'})


urlpatterns = [
    path('create-superuser/', create_superuser),  # ← TEMPORARY, DELETE AFTER USE
    path('admin/', admin.site.urls),
    path('api/register/', register_view, name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/logout/', logout_view, name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('books.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('api/verify-email/<uidb64>/<token>/', verify_email, name='verify-email'),
]