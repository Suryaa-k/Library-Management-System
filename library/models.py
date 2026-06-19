from django.db import models
from django.utils import timezone


class Book(models.Model):
    GENRE_CHOICES = [
        ('Spirituality', 'Spirituality'), ('Mythology', 'Mythology'),
        ('Fiction', 'Fiction'), ('Romance', 'Romance'),
        ('Classic Fiction', 'Classic Fiction'), ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'), ('Fantasy', 'Fantasy'),
        ('Dystopian', 'Dystopian'), ('Self-Help', 'Self-Help'),
        ('Finance', 'Finance'), ('Philosophy', 'Philosophy'),
        ('Non-Fiction', 'Non-Fiction'), ('Biography', 'Biography'),
        ('History', 'History'),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=50, unique=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='Fiction')
    series = models.CharField(max_length=255, blank=True)
    publication_year = models.IntegerField(default=2020)
    shelf_location = models.CharField(max_length=20)
    cover_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} — {self.author}"

    @property
    def available_copies(self):
        return self.copies.filter(status='Available').count()

    @property
    def lent_copies(self):
        return self.copies.filter(status='Lent Out').count()

    @property
    def maintenance_copies(self):
        return self.copies.filter(status='Maintenance').count()

    @property
    def total_copies(self):
        return self.copies.count()


class BookCopy(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Lent Out', 'Lent Out'),
        ('Maintenance', 'Maintenance'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    copy_code = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.book.title} — Copy #{self.copy_code} [{self.status}]"


class Visitor(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    aadhaar_masked = models.CharField(max_length=20, default='XXXX XXXX XXXX')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    @property
    def active_loans_count(self):
        return self.loans.filter(returned_date__isnull=True).count()


class Loan(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Returned On-Time', 'Returned On-Time'),
        ('Returned Late', 'Returned Late'),
    ]
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='loans')
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='loans')
    issued_date = models.DateField()
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.visitor.full_name} -> {self.book_copy.book.title}"

    @property
    def is_overdue(self):
        if self.returned_date:
            return False
        return timezone.now().date() > self.due_date

    def process_return(self):
        today = timezone.now().date()
        self.returned_date = today
        self.status = 'Returned Late' if today > self.due_date else 'Returned On-Time'
        self.book_copy.status = 'Available'
        self.book_copy.save()
        self.save()
