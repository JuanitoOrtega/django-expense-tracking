from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import UserPreference
from apps.expenses.models import Category
import json
# import pdb


@login_required(login_url='login')
def user_preferences(request):
    user = request.user
    user_preference = UserPreference.objects.filter(user=user).first()

    if request.method == 'POST':
        if 'currency' in request.POST:
            # Procesar el formulario de preferencias de moneda
            currency = request.POST.get('currency')
            if currency:
                if user_preference is None:
                    user_preference = UserPreference(user=user, currency=currency)
                else:
                    user_preference.currency = currency
                user_preference.save()
                messages.success(request, 'Configuración de moneda guardada exitosamente')
                return redirect('user_preferences')

        if 'category' in request.POST:
            # Procesar el formulario de creación de categorías
            color = request.POST.get('color')
            category = request.POST.get('category')

            if color and category:
                Category.objects.create(name=category, color=color, owner=user)
                messages.success(request, 'Categoría guardada exitosamente')
                return redirect('user_preferences')

    currency_data = []
    file_path = settings.BASE_DIR / 'currencies.json'

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    categories = Category.objects.filter(owner=user)

    context = {
        'currencies': currency_data,
        'user_preference': user_preference,
        'categories': categories,
    }

    return render(request, 'userpreferences/index.html', context)