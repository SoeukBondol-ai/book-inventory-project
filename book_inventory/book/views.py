from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(name__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'book/book_list.html', {'page_obj': page_obj, 'query': query})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book/book_detail.html', {'book': book})

@login_required
@user_passes_test(lambda u: u.is_admin)
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book/book_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'book/book_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book/book_confirm_delete.html', {'book': book})
