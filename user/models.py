from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Field used for authentication
    USERNAME_FIELD = 'email'

    # Additional fields required when using createsuperuser (USERNAME_FIELD and passwords are always required)
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)
    is_client = models.BooleanField(default=False)  # Add the new field

    def __str__(self):
        return self.username
