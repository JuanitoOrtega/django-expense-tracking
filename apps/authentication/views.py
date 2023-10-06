from django.shortcuts import render
from django.views import View


# Create your views here.
def login(request):
    return render(request, 'authentication/login.html')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')


def reset_password(request):
    return render(request, 'authentication/new_password.html')