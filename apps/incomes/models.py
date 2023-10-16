from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class IncomeSource(models.Model):
    name = models.CharField(max_length=255, verbose_name='Categoría')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Fuente'
        verbose_name_plural = 'Fuentes'

    def __str__(self):
        return self.name


class Income(models.Model):
    amount = models.FloatField(verbose_name='Monto')
    date = models.DateField(default=now, verbose_name='Fecha')
    description = models.TextField(blank=True, null=True, verbose_name='Detalle')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    source = models.ForeignKey(IncomeSource, on_delete=models.CASCADE, verbose_name='Fuente')

    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        ordering: ['-date']

    def __str__(self):
        return self.owner.username
