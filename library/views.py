from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Book, BookCopy, Visitor, Loan
from .forms import BookForm, VisitorForm, LoanForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'library/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    active_loans = Loan.objects.filter(returned_date__isnull=True).select_related('book_copy__book', 'visitor')
    overdue_loans = [l for l in active_loans if l.is_overdue]
    recent_loans = Loan.objects.select_related('book_copy__book', 'visitor').order_by('-created_at')[:8]
    context = {
        'total_titles': Book.objects.count(),
        'total_copies': BookCopy.objects.count(),
        'active_loan_count': active_loans.count(),
        'overdue_count': len(overdue_loans),
        'total_visitors': Visitor.objects.count(),
        'overdue_loans': overdue_loans,
        'recent_loans': recent_loans,
    }
    return render(request, 'library/dashboard.html', context)


@login_required
def book_list(request):
    qs = Book.objects.prefetch_related('copies')
    q = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(isbn__icontains=q))
    if genre:
        qs = qs.filter(genre=genre)
    genres = Book.objects.values_list('genre', flat=True).distinct().order_by('genre')
    return render(request, 'library/book_list.html', {
        'books': qs, 'genres': genres, 'q': q, 'selected_genre': genre,
    })


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    loans = Loan.objects.filter(book_copy__book=book).select_related('visitor', 'book_copy').order_by('-created_at')
    return render(request, 'library/book_detail.html', {'book': book, 'loans': loans})


@login_required
def book_add(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save()
        BookCopy.objects.create(book=book, copy_code=f'{book.pk}a')
        messages.success(request, f'"{book.title}" added with 1 copy!')
        return redirect('book_detail', pk=book.pk)
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Add New Book'})


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, f'"{book.title}" updated!')
        return redirect('book_detail', pk=book.pk)
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Edit Book', 'book': book})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" deleted.')
        return redirect('book_list')
    return render(request, 'library/confirm_delete.html', {
        'object': book, 'object_type': 'Book', 'cancel_url': f'/books/{pk}/',
    })


@login_required
def add_copy(request, pk):
    book = get_object_or_404(Book, pk=pk)
    count = book.copies.count()
    BookCopy.objects.create(book=book, copy_code=f'{book.pk}{chr(97 + count)}')
    messages.success(request, 'New copy added.')
    return redirect('book_detail', pk=pk)


@login_required
def visitor_list(request):
    qs = Visitor.objects.all()
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(Q(full_name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q))
    return render(request, 'library/visitor_list.html', {'visitors': qs, 'q': q})


@login_required
def visitor_detail(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    loans = visitor.loans.select_related('book_copy__book').order_by('-created_at')
    return render(request, 'library/visitor_detail.html', {'visitor': visitor, 'loans': loans})


@login_required
def visitor_add(request):
    form = VisitorForm(request.POST or None)
    if form.is_valid():
        visitor = form.save()
        messages.success(request, f'"{visitor.full_name}" registered!')
        return redirect('visitor_detail', pk=visitor.pk)
    return render(request, 'library/visitor_form.html', {'form': form, 'action': 'Register Visitor'})


@login_required
def visitor_edit(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    form = VisitorForm(request.POST or None, instance=visitor)
    if form.is_valid():
        form.save()
        messages.success(request, f'"{visitor.full_name}" updated!')
        return redirect('visitor_detail', pk=visitor.pk)
    return render(request, 'library/visitor_form.html', {
        'form': form, 'action': 'Edit Visitor', 'visitor': visitor,
    })


@login_required
def visitor_delete(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    if request.method == 'POST':
        name = visitor.full_name
        for loan in visitor.loans.filter(returned_date__isnull=True):
            loan.process_return()
        visitor.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('visitor_list')
    return render(request, 'library/confirm_delete.html', {
        'object': visitor, 'object_type': 'Visitor', 'cancel_url': f'/visitors/{pk}/',
    })


@login_required
def loan_list(request):
    active = Loan.objects.filter(returned_date__isnull=True).select_related('book_copy__book', 'visitor')
    returned = Loan.objects.filter(returned_date__isnull=False).select_related('book_copy__book', 'visitor')
    return render(request, 'library/loan_list.html', {
        'active_loans': active, 'returned_loans': returned,
    })


@login_required
def issue_book(request):
    form = LoanForm(request.POST or None, initial={'issued_date': timezone.now().date()})
    if form.is_valid():
        loan = form.save(commit=False)
        loan.status = 'Active'
        loan.save()
        loan.book_copy.status = 'Lent Out'
        loan.book_copy.save()
        messages.success(request, f'Book issued to {loan.visitor.full_name}!')
        return redirect('loan_list')
    return render(request, 'library/loan_form.html', {'form': form})


@login_required
def process_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        loan.process_return()
        messages.success(request, f'"{loan.book_copy.book.title}" returned!')
        return redirect(request.POST.get('next', 'loan_list'))
    return render(request, 'library/confirm_return.html', {'loan': loan})
