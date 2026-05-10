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
from .views import BookViewSet, CategoryViewSet, register_view, logout_view
from books.views import reset_password_page
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('register/', register_view),
    path('logout/', logout_view),
    path('reset-password/<str:token>/', reset_password_page),
]