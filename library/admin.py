from django.contrib import admin
from .models import Book, BookCopy, Visitor, Loan

class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'shelf_location', 'available_copies', 'total_copies']
    list_filter = ['genre']
    search_fields = ['title', 'author', 'isbn']
    inlines = [BookCopyInline]

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'age', 'registered_at']
    search_fields = ['full_name', 'email', 'phone']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book_copy', 'visitor', 'issued_date', 'due_date', 'returned_date', 'status']
    list_filter = ['status']
    search_fields = ['visitor__full_name', 'book_copy__book__title']

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['copy_code', 'book', 'status']
    list_filter = ['status']
