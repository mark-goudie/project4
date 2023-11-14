from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post (models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    def __str__(self):
        return f"{self.user} posted {self.post} on {self.timestamp}"

class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userextended')
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username