from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username