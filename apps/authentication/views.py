import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'El correo electrónico es inválido'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_exists': 'El correo electrónico ya existe, por favor ingresa uno diferente'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'El usuario solo puede contener caracteres alfanuméricos'}, status=400)

        if len(username) < 4:
            return JsonResponse({'username_error': 'El usuario debe tener al menos 4 caracteres'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_exists': 'El usuario ya existe, por favor ingresa uno diferente'}, status=409)

        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # Create a user account
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                # path_to_view
                # - getting domain we are on
                # - relative url to verification
                # - encode uuid
                # - token

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs = {
                    'uidb64': uidb64,
                    'token': account_activation_token.make_token(user)
                })

                activate_url = 'http://' + domain + link

                email_subject = 'Activa tu cuenta'
                email_body = 'Hola ' + user.username + '. Por favor usa este enlace para verificar tu cuenta.\n' + activate_url

                email = EmailMessage(
                    email_subject,
                    email_body,
                    "ortegaj83@gmail.com",
                    [email],
                    reply_to=["ortegaj83@gmail.com"],
                )

                email.send(fail_silently=False)

                messages.success(request, 'Cuenta registrada exitosamente')

                return render(request, 'authentication/register.html', context)

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id_bytes = urlsafe_base64_decode(uidb64)
            id_str = id_bytes.decode('utf-8')
            user = User.objects.get(pk=id_str)

            if not account_activation_token.check_token(user, token):
                messages.info(request, 'Usuario ya activado')
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Cuenta activada exitosamente')
                else:
                    messages.info(request, 'La cuenta ya está activada')

            return redirect('login')

        except Exception:
            messages.error(request, 'Error al activar la cuenta')

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)

                    messages.success(request, f'Bienvenido, {user.username}, ahora estás conectado.')
                    return redirect('expenses')
                else:
                    messages.warning(request, 'Tu cuenta aún no ha sido activada, por favor revisa tu correo electrónico')

                return render(request, 'authentication/login.html')

            messages.error(request, 'Credenciales inválidas, por favor intenta nuevamente')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Por favor completa todos los campos')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Has cerrado sesión exitosamente.')
        return redirect('login')


def reset_password(request):
    return render(request, 'authentication/new_password.html')