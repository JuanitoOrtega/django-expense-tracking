import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from apps.userpreferences.models import UserPreference


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__name__icontains=search_str, owner=request.user)
        data = list(expenses.values('id', 'amount', 'date', 'description', 'category__name'))
        return JsonResponse(list(data), safe=False)


@login_required(login_url='login')
def expenses(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    items_per_page = 5
    paginator = Paginator(expenses, items_per_page)

    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    currency = UserPreference.objects.get(user=request.user).currency

    context = {
        'expenses': page,
        'currency': currency,
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
            return redirect('expenses')
        except Category.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe')
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error: {str(e)}')

    categories = Category.objects.filter(owner=request.user)
    current_date = date.today()

    context = {
        'categories': categories,
        'current_date': current_date,
    }

    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='login')
def edit_expense(request, expense_id):
    user = request.user
    expense = get_object_or_404(Expense, id=expense_id, owner=user)

    if request.method == 'POST':
        category_id = request.POST['category']
        amount = request.POST['amount']
        description = request.POST['description']
        fecha = request.POST['date']

        try:
            category = Category.objects.get(id=category_id)
            expense.category = category
            expense.amount = amount
            expense.description = description
            expense.date = fecha
            expense.save()
            messages.success(request, 'El gasto se ha actualizado con éxito')
            return redirect('expenses')
        except Category.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe')
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error: {str(e)}')

    categories = Category.objects.filter(owner=user)

    context = {
        'expense': expense,
        'categories': categories,
    }

    return render(request, 'expenses/edit_expense.html', context)


@login_required(login_url='login')
def delete_expense(request, expense_id):
    user = request.user

    # Obtén el objeto Expense que deseas eliminar, asegurándote de que pertenezca al usuario en sesión
    expense = get_object_or_404(Expense, id=expense_id, owner=user)

    if request.method == 'POST':
        try:
            expense.delete()
            messages.success(request, 'El gasto ha sido eliminado con éxito')
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al eliminar el gasto: {str(e)}')

        return redirect('expenses')

    context = {
        'expense': expense,
    }

    return render(request, 'expenses/delete_expense.html', context)