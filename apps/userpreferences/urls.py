from django.urls import path
from .views import user_preferences


urlpatterns = [
    path('', user_preferences, name='user_preferences'),
]
