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
        context['categories'] = Category.objects.all()
        context['new_arrivals'] = Book.objects.filter(is_new_arrival=True)[:6]
        context['best_sellers'] = Book.objects.filter(is_best_seller=True)[:6]
        context['now_trending'] = Book.objects.filter(is_now_trending=True)[:6]
        context['award_winners'] = Book.objects.filter(is_award_winner=True)[:6]
        for category in context['categories']:
            context[f'{category.name.lower().replace(" ", "_")}_books'] = Book.objects.filter(category=category)[:6]
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get current book
        book = self.get_object()
        context['related_books'] = Book.objects.filter(
            category=book.category
        ).exclude(id=book.id)[:4]
        
        return context

class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'
    def get_queryset(self):
        queryset = Book.objects.all().order_by('title')  
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

def search_books(request):
    query = request.GET.get('q', ' ')
    books = []
    if query:
        books = Book.objects.filter(Q(title__icontains=query)|Q(author__icontains=query)).order_by('title')
    return render(request, 'book/search_results.html', {'books': books, 'query': query})

def book_list_by_category(request, category):
    """Display books filtered by category"""
    category_filters = {
        'new-arrivals': ('New Arrivals', Q(is_new_arrival=True)),
        'now-trending': ('Now Trending', Q(is_now_trending=True)),
        'best-sellers': ('Best Sellers', Q(is_best_seller=True)),
        'award-winners': ('Award Winners', Q(is_award_winner=True))
    }

    if category in category_filters:
        display_name, query = category_filters[category]
        books = Book.objects.filter(query)
    else:
        display_name = category.replace('-', ' ').title()
        books = Book.objects.filter(category__name__iexact=display_name)

    paginator = Paginator(books.order_by('title'), 12)
    page = request.GET.get('page', 1)
    books_page = paginator.get_page(page)

    return render(request, 'book/book_list.html', {
        'books': books_page,
        'category': display_name,
        'categories': Category.objects.all()
    })

def get_categories(request):
    return {'categories': Category.objects.all()}
