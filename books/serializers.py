from rest_framework import serializers
from .models import Book, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields="__all__"
class BookSerializer(serializers.ModelSerializer):
    category_name= serializers.ReadOnlyField(source="category.name")
    class Meta:
        model= Book
        fields= [
            'id','title','author','published_date','isbn','category','category_name'
        ]
