from django.urls import path
from .views import EmailValidationView, UsernameValidationView, LoginView, LogoutView, RegistrationView, VerificationView, reset_password
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('set-new-password/', reset_password, name='reset-password'),
]
