from django.contrib import admin

# Register your models here.
from .models import Book, Category, Profile

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Profile)
