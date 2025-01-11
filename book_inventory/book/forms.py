from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'stock', 'description', 'image', 'category', 'is_new_arrival', 'is_best_seller', 'is_now_trending', 'is_award_winner']