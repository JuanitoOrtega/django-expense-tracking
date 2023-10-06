from django.urls import path
from .views import login, RegistrationView, reset_password


urlpatterns = [
    path('login/', login, name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('set-new-password/', reset_password, name='reset_password'),
]
