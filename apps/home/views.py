from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.expenses.models import Expense
from django.http import JsonResponse
import datetime
import json


@login_required(login_url='login')
def home(request):

    context = {
        'title': 'Bienvenido a My Wallet',
    }

    return render(request, 'home.html', context)