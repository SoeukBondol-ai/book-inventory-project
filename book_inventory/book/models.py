from django.db import models
from django.conf import settings

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.name
