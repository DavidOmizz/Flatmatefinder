from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name() or self.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        initials = (self.first_name[0] if self.first_name else self.username[0]).upper()
        return f"https://ui-avatars.com/api/?name={self.get_full_name() or self.username}&background=2d6a4f&color=fff&size=128"
