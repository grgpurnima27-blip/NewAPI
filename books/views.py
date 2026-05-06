from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Book, Category
# from serializers import BookSerializer, CategorySerializer
from .serializers import *
# Create your views here.
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset= Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class= CategorySerializer
    permission_classes=[IsAuthenticated]

    from django.shortcuts import render

def reset_password_page(request, token):
    return render(request, 'reset_password.html', {'token': token})
