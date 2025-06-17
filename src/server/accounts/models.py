from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    studiengang = models.CharField(max_length=100, blank=True)
    gruppe = models.CharField(max_length=20, blank=True)
    rolle = models.IntegerField(null=True, blank=True)
