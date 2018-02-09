from django.db import models
from django.contrib.auth.models import User


# admin qwert123
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    deleted = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Id: {} Title: {}'.format(self.id, self.title)


class Comment(models.Model):
    body = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return 'Comment: {}'.format(self.body[:30])


class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return 'UserID: {} PostID: {}'.format(self.user_id, self.post_id)
