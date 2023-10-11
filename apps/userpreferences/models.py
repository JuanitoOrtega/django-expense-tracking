from django.db import models
from django.contrib.auth.models import User


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    currency = models.CharField(max_length=3, blank=True, null=True, verbose_name='Moneda')

    class Meta:
        verbose_name = 'Preferencias de usuario'
        verbose_name_plural = 'Preferencias de usuarios'

    def __str__(self):
        return self.user.username
