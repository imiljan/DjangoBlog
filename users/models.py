from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Comment, Post


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='static/img', default='static/img/man.png')

    def __str__(self):
        return 'Username: {} \n Bio: {}'.format(self.user.username, self.bio)

    @property
    def no_of_likes(self):
        return sum(Post.objects.values_list('likes', flat=True).filter(user_id=self.user.pk))

    @property
    def no_of_comments(self):
        posts_by_user = Post.objects.values_list('id', flat=True).filter(user_id=self.user.pk)
        suma = 0
        for p in posts_by_user:
            temp = Comment.objects.filter(post_id=p).count()
            suma += temp
        return suma

    @property
    def no_of_views(self):
        return sum(Post.objects.values_list('views', flat=True).filter(user_id=self.user.pk))


@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_details(sender, instance, **kwargs):
    instance.userdetails.save()
