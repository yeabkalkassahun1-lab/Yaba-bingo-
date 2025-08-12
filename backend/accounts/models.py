# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
import decimal

class Agent(AbstractUser):
    operational_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username