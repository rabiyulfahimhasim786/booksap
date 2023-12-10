from django.db import models

# Create your models here.
# from django.db import models
# author models
class Author(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    publication_year = models.DateField(null=True, blank=True)
    # nationality = models.CharField(max_length=100, null=True, blank=True)

    # Add more author-related fields as needed
# Book models
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    is_active = models.BooleanField(default=True)
    # Add more book-related fields as needed
# Review models
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
