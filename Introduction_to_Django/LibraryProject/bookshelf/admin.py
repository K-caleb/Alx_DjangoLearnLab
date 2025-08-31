from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the Book model.
    """
    # Display the specified fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters for easier searching by publication year
    list_filter = ('publication_year',)
    
    # Add search capability for title and author
    search_fields = ('title', 'author')

# Register the Book model with the custom admin configuration
admin.site.register(Book, BookAdmin)
