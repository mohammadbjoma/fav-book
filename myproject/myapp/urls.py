from django.urls import path
from . import views

urlpatterns = [
    # Authentication routes
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    
    # Book routes
    path('books', views.books),
    path('books/add', views.add_book),
    path('books/<int:book_id>', views.book_details),
    path('books/<int:book_id>/favorite', views.favorite_book),
    path('books/<int:book_id>/unfavorite', views.unfavorite_book),
    path('books/<int:book_id>/edit', views.edit_book),
    path('books/<int:book_id>/update', views.update_book),
    path('books/<int:book_id>/delete', views.delete_book),
    
    # User favorites 
    path('favorites', views.user_favorites),
]