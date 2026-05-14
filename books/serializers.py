from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Category, Profile


# REGISTER

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email    = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# LOGOUT

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)


# CATEGORY

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = "__all__"


# BOOK

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model  = Book
        fields = [
            "id",
            "title",
            "author",
            "published_date",
            "isbn",
            "category",
            "category_name",
            "created_at",
        ]
        read_only_fields = ["created_at"]


# PROFILE

class ProfileSerializer(serializers.ModelSerializer):
    username            = serializers.ReadOnlyField(source="user.username")
    email               = serializers.ReadOnlyField(source="user.email")
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model  = Profile
        fields = [
            "id",
            "username",
            "email",
            "profile_picture",
            "profile_picture_url",
            "created_at",
        ]
        read_only_fields = ["id", "username", "email", "profile_picture_url", "created_at"]

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None