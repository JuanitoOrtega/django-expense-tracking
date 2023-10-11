from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from datetime import date


@login_required(login_url='login')
def expenses(request):

    user = request.user
    expenses = Expense.objects.all(user)

    context = {
        'expenses': expenses,
    }

    return render(request, 'expenses/home.html', context)


@login_required(login_url='login')
def add_expense(request):
    user = request.user
    if request.method == 'POST':
        category_id = request.POST['category']
        amount = request.POST['amount']
        description = request.POST['description']
        fecha = request.POST['date']

        try:
            category = Category.objects.get(id=category_id)
            Expense.objects.create(owner=user, category=category, amount=amount, description=description, date=fecha)
            messages.success(request, 'El gasto se ha guardado con éxito')
            return redirect('add_expense')
        except Category.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe')
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error: {str(e)}')

    categories = Category.objects.all(user)
    current_date = date.today()

    context = {
        'categories': categories,
        'current_date': current_date,
    }

    return render(request, 'expenses/add_expense.html', context)
