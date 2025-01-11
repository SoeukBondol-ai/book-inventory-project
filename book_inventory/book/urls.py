from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<str:category>/', views.book_list_by_category, name='book_list_by_category'),
    path('search/', views.search_books, name='search_books'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),
]