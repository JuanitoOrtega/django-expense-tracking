from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from apps.managers import ObjectsManager


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Categoría')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')

    objects = ObjectsManager()

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.FloatField(verbose_name='Monto')
    date = models.DateField(default=now, verbose_name='Fecha')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')

    objects = ObjectsManager()

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering: ['-date']

    def __str__(self):
        return self.owner.username
