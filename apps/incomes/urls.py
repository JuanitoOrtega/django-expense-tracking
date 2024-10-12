from django.urls import path
from .views import search_incomes, incomes, add_income, edit_income, delete_income
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', incomes, name='incomes'),
    path('search-incomes/', csrf_exempt(search_incomes), name='search_incomes'),
    path('add-income/', add_income, name='add_income'),
    path('edit/<int:income_id>/', edit_income, name='edit_income'),
    path('delete/<int:income_id>/', delete_income, name='delete_income'),
]
