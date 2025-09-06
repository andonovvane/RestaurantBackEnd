from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ('client', 'Client'),
        ('waiter', 'Waiter'),
        ('kitcher', 'Kitcher'),
        ('ceo', 'CEO'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    table_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})" if self.role else self.username
