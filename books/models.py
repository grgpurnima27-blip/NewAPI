from django.db import models

# Create your models here.
class Category(models.Model):
    name= models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title= models.CharField(max_length=52)
    author=models.CharField(max_length=50)
    published_date= models.DateField()
    isbn= models.CharField(max_length=13, unique=True, null=True, blank=True)

    category= models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books"
    )

    def __str__(self):
        return self.title
