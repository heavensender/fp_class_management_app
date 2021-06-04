from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    sex = models.IntegerField(verbose_name="Gender", choices=((0, 'Male'), (1, 'Female')), default=0)
    phone = models.CharField(verbose_name="Phone", null=True, max_length=8)
    address = models.CharField(verbose_name="Address", null=True, max_length=255)

    def __str__(self):
        return self.username

