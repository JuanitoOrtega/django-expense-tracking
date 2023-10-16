from django.contrib import admin
from .models import Category, Expense


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'description', 'owner', 'category', 'date']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)