from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'expenses/home.html')


def add_expense(request):
    return render(request, 'expenses/add_expense.html')