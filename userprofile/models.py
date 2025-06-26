from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

