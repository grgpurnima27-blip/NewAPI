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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet, register_view, logout_view, test_email

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('test-email/', test_email, name='test-email'),
]