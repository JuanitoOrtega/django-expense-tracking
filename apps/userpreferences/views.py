from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import UserPreference
import json
# import pdb


@login_required(login_url='login')
def index(request):
    user_preference = UserPreference.objects.filter(user=request.user).first()

    if request.method == 'POST':
        currency = request.POST.get('currency')
        if currency:
            if user_preference is None:
                user_preference = UserPreference(user=request.user, currency=currency)
            else:
                user_preference.currency = currency
            user_preference.save()
            messages.success(request, 'Configuración guardada exitosamente')
            return redirect('preferences')

    currency_data = []
    file_path = settings.BASE_DIR / 'currencies.json'

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    context = {
        'currencies': currency_data,
        'user_preference': user_preference,
    }

    return render(request, 'userpreferences/index.html', context)