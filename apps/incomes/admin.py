from django.contrib import admin
from .models import IncomeSource, Income


class IncomeSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'owner', 'source', 'date')


admin.site.register(IncomeSource, IncomeSourceAdmin)
admin.site.register(Income, IncomeAdmin)