from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Post(models.Model):
    title = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes')
    image = models.ImageField(upload_to="post-images", null=True)
    comments = models.ManyToManyField(Comment, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title