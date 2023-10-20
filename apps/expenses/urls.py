from django.urls import path
from .views import search_expenses, expenses, add_expense, edit_expense, delete_expense, expense_category_summary, expense_summary, export_csv, export_excel, export_pdf
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', expenses, name='expenses'),
    path('search-expenses/', csrf_exempt(search_expenses), name='search_expenses'),
    path('add-expense/', add_expense, name='add_expense'),
    path('edit/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('expense-category-summary/', expense_category_summary, name='expense_category_summary'),
    path('expense-summary/', expense_summary, name='expense_summary'),
    path('export-csv/', export_csv, name='export_csv'),
    path('export-excel/', export_excel, name='export_excel'),
    path('export-pdf/', export_pdf, name='export_pdf'),
]
