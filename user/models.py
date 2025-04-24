from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    photo = models.ImageField(upload_to="user/%Y/%m/%d", null=True, blank=True, verbose_name="Photo")
    date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name="Дата рождение")

    def get_absolute_url(self):
        return reverse("user", kwargs={"username": self.username})
