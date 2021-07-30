from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='display-pictures', null=True)
    followers = models.ManyToManyField(User, related_name='followers')
    following = models.ManyToManyField(User, related_name='following')
    bookmark = models.ManyToManyField(Post, related_name='bookmark')

    def __str__(self):
        return self.user.username