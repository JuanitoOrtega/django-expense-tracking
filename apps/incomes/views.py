import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Income, IncomeSource
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from datetime import date
from django.http import JsonResponse


def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__name__icontains=search_str, owner=request.user)
        data = list(incomes.values('id', 'amount', 'date', 'description', 'source__name'))
        return JsonResponse(list(data), safe=False)


@login_required(login_url='login')
def incomes(request):
    incomes = Income.objects.filter(owner=request.user).order_by('-date')
    items_per_page = 5
    paginator = Paginator(incomes, items_per_page)

    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'incomes': page,
    }

    return render(request, 'incomes/home.html', context)


@login_required(login_url='login')
def add_income(request):
    user = request.user
    if request.method == 'POST':
        source_id = request.POST['source']
        amount = request.POST['amount']
        description = request.POST['description']
        fecha = request.POST['date']

        try:
            source = IncomeSource.objects.get(id=source_id)
            Income.objects.create(owner=user, source=source, amount=amount, description=description, date=fecha)
            messages.success(request, 'El ingreso se ha guardado con éxito')
            return redirect('incomes')
        except IncomeSource.DoesNotExist:
            messages.error(request, 'La fuente de ingresos seleccionada no existe')
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error: {str(e)}')

    sources = IncomeSource.objects.filter(owner=request.user)
    current_date = date.today()

    context = {
        'sources': sources,
        'current_date': current_date,
    }

    return render(request, 'incomes/add_income.html', context)


@login_required(login_url='login')
def edit_income(request, income_id):
    user = request.user
    income = get_object_or_404(Income, id=income_id, owner=user)

    if request.method == 'POST':
        source_id = request.POST['source']
        amount = request.POST['amount']
        description = request.POST['description']
        fecha = request.POST['date']

        try:
            source = IncomeSource.objects.get(id=source_id)
            income.source = source
            income.amount = amount
            income.description = description
            income.date = fecha
            income.save()
            messages.success(request, 'Ingreso actualizado con éxito')
            return redirect('incomes')
        except IncomeSource.DoesNotExist:
            messages.error(request, 'La fuente del ingreso seleccionada no existe')
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error: {str(e)}')

    sources = IncomeSource.objects.filter(owner=user)

    context = {
        'income': income,
        'sources': sources,
    }

    return render(request, 'incomes/edit_income.html', context)


@login_required(login_url='login')
def delete_income(request, income_id):
    user = request.user

    # Obtén el objeto Income que deseas eliminar, asegurándote de que pertenezca al usuario en sesión
    income = get_object_or_404(Income, id=income_id, owner=user)

    if request.method == 'POST':
        try:
            income.delete()
            messages.success(request, 'Ingreso eliminado con éxito')
        except Exception as e:
            messages.error(request, f'Ha ocurrido un error al eliminar el ingreso: {str(e)}')

        return redirect('incomes')

    context = {
        'income': income,
    }

    return render(request, 'incomes/delete_income.html', context)