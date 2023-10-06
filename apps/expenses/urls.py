from django.urls import path
from .views import home, add_expense


urlpatterns = [
    path('', home, name='home'),
    path('add-expense/', add_expense, name='add_expense'),
]
