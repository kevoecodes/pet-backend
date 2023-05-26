from django.conf import settings
from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=255)
    device_no = models.CharField(max_length=255, unique=True)

    active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PetLocation(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    longitudes = models.FloatField()
    latitudes = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

