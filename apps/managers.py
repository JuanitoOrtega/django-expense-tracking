from django.db import models


class ObjectsManager(models.Manager):
    def all(self, user):
        return super().get_queryset().filter(owner=user)