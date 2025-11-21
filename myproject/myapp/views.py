from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    """Handle user registration"""
    if request.method == "POST":
        # Validate form data
        errors = User.objects.validator(request.POST)
        
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        # Hash password
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), 
            bcrypt.gensalt()
        ).decode()
        
        # Create user
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hashed_pw
        )
        
        # Store user id in session
        request.session['user_id'] = user.id
        messages.success(request, "Successfully registered!")
        return redirect('/books')
    
    return redirect('/')


def login(request):
    """Handle user login"""
    if request.method == "POST":
        # Check if user exists
        user = User.objects.filter(email=request.POST['email'])
        
        if user:
            logged_user = user[0]
            # Check password
            if bcrypt.checkpw(
                request.POST['password'].encode(), 
                logged_user.password.encode()
            ):
                request.session['user_id'] = logged_user.id
                return redirect('/books')
        
        messages.error(request, "Invalid email or password")
        return redirect('/')
    
    return redirect('/')


def logout(request):
    """Handle user logout"""
    request.session.flush()
    return redirect('/')


# ============= Book Views =============

def books(request):
    """Display main books page"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_books': Book.objects.all()
    }
    return render(request, 'books.html', context)


def add_book(request):
    """Handle adding a new book"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    if request.method == "POST":
        errors = Book.objects.validator(request.POST)
        
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        
        # Get logged in user
        user = User.objects.get(id=request.session['user_id'])
        
        # Create book
        book = Book.objects.create(
            title=request.POST['title'],
            desc=request.POST['desc'],
            uploaded_by=user
        )
        
        # Automatically favorite the book for the uploader
        book.users_who_like.add(user)
        
        messages.success(request, "Book added successfully!")
        return redirect('/books')
    
    return redirect('/books')


def book_details(request, book_id):
    """Display details for a specific book"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'book': Book.objects.get(id=book_id)
    }
    return render(request, 'book_details.html', context)


def favorite_book(request, book_id):
    """Add a book to user's favorites"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    book.users_who_like.add(user)
    
    return redirect(request.META.get('HTTP_REFERER', '/books'))


def unfavorite_book(request, book_id):
    """Remove a book from user's favorites"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    book.users_who_like.remove(user)
    
    return redirect(request.META.get('HTTP_REFERER', '/books'))


def edit_book(request, book_id):
    """Display edit form for a book"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    book = Book.objects.get(id=book_id)
    
    # Check if user is the uploader
    if book.uploaded_by.id != request.session['user_id']:
        return redirect('/books')
    
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'book': book
    }
    return render(request, 'edit_book.html', context)


def update_book(request, book_id):
    """Handle updating a book"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    if request.method == "POST":
        errors = Book.objects.validator(request.POST)
        
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/books/{book_id}/edit')
        
        book = Book.objects.get(id=book_id)
        
        # Check if user is the uploader
        if book.uploaded_by.id != request.session['user_id']:
            return redirect('/books')
        
        book.title = request.POST['title']
        book.desc = request.POST['desc']
        book.save()
        
        messages.success(request, "Book updated successfully!")
        return redirect(f'/books/{book_id}')
    
    return redirect('/books')


def delete_book(request, book_id):
    """Handle deleting a book"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    book = Book.objects.get(id=book_id)
    
    # Check if user is the uploader
    if book.uploaded_by.id == request.session['user_id']:
        book.delete()
        messages.success(request, "Book deleted successfully!")
    
    return redirect('/books')


def user_favorites(request):
    """SENSEI BONUS: Display user's favorite books"""
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'favorites.html', context)