from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Book, Category
from django.core.paginator import Paginator

class HomeView(ListView):
    model = Book
    template_name = 'book/home.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_arrivals'] = Book.objects.filter(is_new_arrival=True)[:6]
        context['best_sellers'] = Book.objects.filter(is_best_seller=True)[:6]
        context['now_trending'] = Book.objects.filter(is_now_trending=True)[:6]
        context['award_winners'] = Book.objects.filter(is_award_winner=True)[:6]
        context['categories'] = Category.objects.all()
        for category in context['categories']:
            context[f'{category.name.lower().replace(" ", "_")}_books'] = Book.objects.filter(category=category)[:6]
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'

class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category = self.kwargs.get('category')
        if category:
            context['category'] = category
        return context

def search_books(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by('title')
    return render(request, 'book/search_results.html', {'books': books, 'query': query})

def book_list_by_category(request, category):
    if category == 'new-arrivals':
        books = Book.objects.filter(is_new_arrival=True).order_by('title')
    elif category == 'now-trending':
        books = Book.objects.filter(is_now_trending=True).order_by('title')
    elif category == 'best-sellers':
        books = Book.objects.filter(is_best_seller=True).order_by('title')
    elif category == 'award-winners':
        books = Book.objects.filter(is_award_winner=True).order_by('title')
    else:
        books = Book.objects.filter(category__name=category).order_by('title')
    
    paginator = Paginator(books, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'book/book_list.html', {'page_obj': page_obj, 'category': category})

