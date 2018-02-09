from django.contrib.auth.models import User
from django.db import models


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.URLField(blank=True)