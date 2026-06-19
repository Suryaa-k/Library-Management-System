from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('books/<int:pk>/add-copy/', views.add_copy, name='add_copy'),

    # Visitors
    path('visitors/', views.visitor_list, name='visitor_list'),
    path('visitors/add/', views.visitor_add, name='visitor_add'),
    path('visitors/<int:pk>/', views.visitor_detail, name='visitor_detail'),
    path('visitors/<int:pk>/edit/', views.visitor_edit, name='visitor_edit'),
    path('visitors/<int:pk>/delete/', views.visitor_delete, name='visitor_delete'),

    # Loans
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/issue/', views.issue_book, name='issue_book'),
    path('loans/<int:pk>/return/', views.process_return, name='process_return'),
]
