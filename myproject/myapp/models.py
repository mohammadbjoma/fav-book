from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        
        # First name validation
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        
        # Last name validation
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        
        # Email validation
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        else:
            # Check if email already exists (for registration)
            existing_user = User.objects.filter(email=postData['email'])
            if existing_user:
                errors['email'] = "Email already in use"
        
        # Password validation
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        
        # Confirm password validation
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name}>"


class BookManager(models.Manager):
    def validator(self, postData):
        errors = {}
        
        # Title validation
        if len(postData['title']) < 1:
            errors['title'] = "Title is required"
        
        # Description validation
        if len(postData['desc']) < 5:
            errors['desc'] = "Description must be at least 5 characters"
        
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(
        User, 
        related_name="books_uploaded", 
        on_delete=models.CASCADE
    )
    users_who_like = models.ManyToManyField(
        User, 
        related_name="liked_books"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = BookManager()
    
    def __repr__(self):
        return f"<Book: {self.title}>"