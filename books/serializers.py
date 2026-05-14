from rest_framework import serializers
from .models import Book, Category
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email    = serializers.EmailField(required=True)  

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model  = Book
        fields = [
            'id', 'title', 'author', 'published_date', 'isbn', 'category', 'category_name'
        ]