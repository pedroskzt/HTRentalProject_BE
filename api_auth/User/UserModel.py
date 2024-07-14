from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class User(AbstractUser):
    """
    Custom user model with additional fields:
    - Address
    """
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"