from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.URLField(blank=True)


@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_details(sender, instace, **kwargs):
    instace.userdetails.save()
