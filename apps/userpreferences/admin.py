from django.contrib import admin
from .models import UserPreference


class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency']


admin.site.register(UserPreference, UserPreferenceAdmin)