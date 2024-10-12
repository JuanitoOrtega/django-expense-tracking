from django.urls import path
from .views import EmailValidationView, UsernameValidationView, LoginView, LogoutView, RegistrationView, VerificationView, RequestPasswordView, ResetPasswordView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('request-password/', RequestPasswordView.as_view(), name='request_password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
]
