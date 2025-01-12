from django.contrib import admin
from .models import Book, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'category', 'is_new_arrival', 'is_best_seller', 'is_now_trending', 'is_award_winner')
    list_filter = ('category', 'is_new_arrival', 'is_best_seller', 'is_now_trending', 'is_award_winner')
    search_fields = ('title', 'author', 'description')
    list_editable = ('price', 'is_new_arrival', 'is_best_seller', 'is_now_trending', 'is_award_winner')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
from .models import Wishlist  # Import your Wishlist model

admin.site.register(Wishlist)