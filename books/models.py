from django.db import models
from django.contrib.auth.models import User


# CATEGORY MODEL

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# BOOK MODEL

class Book(models.Model):
    title = models.CharField(max_length=52)
    author = models.CharField(max_length=50)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# PROFILE MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)  # stores relative media path
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username