from django.urls import path
from .views import search_expenses, expenses, add_expense, edit_expense, delete_expense
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', expenses, name='expenses'),
    path('search-expenses/', csrf_exempt(search_expenses), name='search_expenses'),
    path('add-expense/', add_expense, name='add_expense'),
    path('edit/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('delete/<int:expense_id>/', delete_expense, name='delete_expense'),
]
