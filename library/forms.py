from django import forms
from .models import Book, BookCopy, Visitor, Loan


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'genre', 'series',
                  'publication_year', 'shelf_location', 'cover_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. The Alchemist'}),
            'author': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Paulo Coelho'}),
            'isbn': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. SVG-0001'}),
            'genre': forms.Select(attrs={'class': 'form-input'}),
            'series': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Leave blank if standalone'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '2024'}),
            'shelf_location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. A-01'}),
            'cover_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://... (optional)'}),
        }


class VisitorForm(forms.ModelForm):
    aadhaar_raw = forms.CharField(
        max_length=12,
        required=False,
        label='Aadhaar Number',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last 4 digits only (e.g. 4521)',
            'maxlength': '12',
        })
    )

    class Meta:
        model = Visitor
        fields = ['full_name', 'age', 'address', 'email', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}),
            'age': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Age'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Residential address'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit mobile number'}),
        }

    def save(self, commit=True):
        visitor = super().save(commit=False)
        raw = self.cleaned_data.get('aadhaar_raw', '')
        last4 = raw[-4:] if raw else '****'
        visitor.aadhaar_masked = f'XXXX XXXX {last4}'
        if commit:
            visitor.save()
        return visitor


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['book_copy', 'visitor', 'issued_date', 'due_date']
        widgets = {
            'book_copy': forms.Select(attrs={'class': 'form-input'}),
            'visitor': forms.Select(attrs={'class': 'form-input'}),
            'issued_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available copies
        self.fields['book_copy'].queryset = BookCopy.objects.filter(
            status='Available'
        ).select_related('book').order_by('book__title')
        self.fields['book_copy'].label_from_instance = lambda obj: f"{obj.book.title} — Copy #{obj.copy_code}"
        self.fields['visitor'].queryset = Visitor.objects.all().order_by('full_name')
