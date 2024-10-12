import json
import datetime
import csv
import xlwt
import tempfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from apps.userpreferences.models import UserPreference
from weasyprint import HTML
from django.db.models import Sum
from django.template.loader import render_to_string


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


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for category in category_list:
        finalrep[category.name] = get_expense_category_amount(category)

    finalrep_json = json.dumps(finalrep)

    return JsonResponse({'expense_category_data': finalrep_json}, safe=False)


def expense_summary(request):
    return render(request, 'expenses/expense_summary.html')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses_' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Monto', 'Descripción', 'Categoría', 'Fecha'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses_' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Monto', 'Descripción', 'Categoría', 'Fecha']

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title, font_style)

    font_style = xlwt.XFStyle()

    expenses = Expense.objects.filter(owner=request.user).values('amount', 'description', 'category__name', 'date')

    for row_num, expense in enumerate(expenses, 1):  # Comienza desde la segunda fila
        ws.write(row_num, 0, expense['amount'], font_style)
        ws.write(row_num, 1, expense['description'], font_style)
        ws.write(row_num, 2, expense['category__name'], font_style)  # Accede al nombre de la categoría
        ws.write(row_num, 3, expense['date'].strftime('%d/%m/%Y'), font_style)  # Formatea la fecha

    wb.save(response)

    return response


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses_' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    user = request.user

    expenses = Expense.objects.filter(owner=user)
    suma = expenses.aggregate(Sum('amount'))

    context = {
        'expenses': expenses,
        'total': suma['amount__sum'],
        'user': user,
    }

    html_string = render_to_string('expenses/pdf/pdf_output.html', context)
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response
