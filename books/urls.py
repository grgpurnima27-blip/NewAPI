from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet, register_view, logout_view, verify_email

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # AUTH
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # EMAIL VERIFICATION (IMPORTANT ADD THIS)
    path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify-email'),
]