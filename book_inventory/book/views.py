from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Book, Category, Wishlist, Cart
from django.core.paginator import Paginator
from .forms import BookForm
from django.contrib.auth.decorators import login_required

class HomeView(ListView):
    model = Book
    template_name = 'book/home.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['new_arrivals'] = Book.objects.filter(is_new_arrival=True)
        context['best_sellers'] = Book.objects.filter(is_best_seller=True)
        context['now_trending'] = Book.objects.filter(is_now_trending=True)
        context['award_winners'] = Book.objects.filter(is_award_winner=True)
        context['random_books'] = Book.objects.order_by('?')[:30]
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['related_books'] = Book.objects.filter(category=book.category).exclude(id=book.id)[:4]
        context['categories'] = Category.objects.all()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def search_books(request):
    query = request.GET.get('q', ' ')
    books = []
    if query:
        books = Book.objects.filter(Q(title__icontains=query)|Q(author__icontains=query)).order_by('title')
    return render(request, 'book/search_results.html', {'books': books, 'query': query})

def book_list_by_category(request, category):
    """### Display books filtered by category"""
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

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')  # run back to home 
    else:
        form = BookForm()
    return render(request, 'book/add_book.html', {'form': form})

@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('/')  # run back to home 
    else:
        form = BookForm(instance=book)
    return render(request, 'book/edit_book.html', {'form': form})

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('/')  # run back to home 
    return render(request, 'book/delete_book.html', {'book': book})

# add book to wishlist
def add_to_wishlist(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        # Check if the book is already in the wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, book=book)
        if created:
            print(f"Added {book.title} to wishlist.")
        else:
            print(f"{book.title} is already in wishlist.")
        # Redirect back to the same page (the page where the user added the book)
        return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect to the referring page or home
    return redirect('login')  # Redirect unauthenticated users to login

# view wishlist page
@login_required
def view_wishlist(request):
    print("Load wishlist page")
    if request.user.is_authenticated:
        print("User is authenticated")
        wishlist_items = Wishlist.objects.filter(user=request.user)
        print(f"Wishlist items: {wishlist_items}")
        return render(request, 'book/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        print("User is not authenticated")
    return redirect('login')  # Redirect unauthenticated users to login

# remove book from wishlist
@login_required
def remove_from_wishlist(request, item_id):
    if request.user.is_authenticated:
        # Get the wishlist item by ID
        wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
        print(f"Deleted: {wishlist_item}")
        wishlist_item.delete()  # Delete the item from the wishlist
        
        wishlist_items = Wishlist.objects.filter(user=request.user)
        print(f"Wishlist items: {wishlist_items}")
        return render(request, 'book/wishlist.html', {'wishlist_items': wishlist_items})
        # return redirect('wishlist')  # Redirect to the wishlist page after deletion
    return redirect('login')  # Redirect unauthenticated users to login


# add book to cart
def add_to_cart(request, book_id):
    if request.user.is_authenticated:
            book = get_object_or_404(Book, id=book_id)
            try:
                # Add or update the cart item
                cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                print(f"Added {book.title} to cart.")
            except Exception as e:
                print(f"Error adding {book.title} to cart: {e}")
            # Redirect back to the same page (the page where the user added the book)
            return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect to the referring page or home
    return redirect('login')  # Redirect unauthenticated users to login
    
# add more to cart
def add_more_to_cart(request, cart_item_id):
    if request.method == 'POST':
        # Get the cart item or return a 404 error if not found
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
        
        # Get the quantity to add from the form
        quantity_to_add = int(request.POST.get('quantity_to_add', 1))
        
        # Ensure the quantity to add is valid
        if quantity_to_add <= 0:
            return redirect('view_cart')  # Do nothing if the quantity is invalid
        
        # Update the cart item's quantity
        cart_item.quantity += quantity_to_add
        cart_item.save()
        
    # Redirect back to the cart page
    return redirect('view_cart')

# view cart
@login_required
def view_cart(request):
    print("Loading cart page for user:", request.user)  # Debugging
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    print(f"Cart items: {cart_items}")  # Debugging
    print(f"Total price: {total_price}")  # Debugging
    return render(request, 'book/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


# remove from cart
@login_required
def remove_from_cart(request, cart_item_id):
    if request.method == 'POST':
        # Get the cart item or return a 404 error if not found
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
        # Get the quantity to remove from the form
        quantity_to_remove = int(request.POST.get('quantity_to_remove', 1))
        # Ensure the quantity to remove is valid
        if quantity_to_remove <= 0:
            return redirect('view_cart')  # Do nothing if the quantity is invalid
        # Update the cart item's quantity
        if quantity_to_remove >= cart_item.quantity:
            # If the quantity to remove is greater than or equal to the current quantity, delete the item
            cart_item.delete()
        else:
            # Otherwise, reduce the quantity
            cart_item.quantity -= quantity_to_remove
            cart_item.save()
    # Redirect back to the cart page
    return redirect('view_cart')