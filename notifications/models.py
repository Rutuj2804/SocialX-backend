from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_by')
    requested_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_to')
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return self.requested_by.username