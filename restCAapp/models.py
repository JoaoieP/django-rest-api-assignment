from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'