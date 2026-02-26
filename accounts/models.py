from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)  # optional login, but not USERNAME_FIELD
    job_title = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username