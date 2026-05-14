from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BookViewSet,
    CategoryViewSet,
    register_view,
    login_view,
    logout_view,
    verify_email,
)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('register/', register_view),
    path('login/', login_view),
    path('logout/', logout_view),

    path('verify-email/<uidb64>/<token>/', verify_email),
]