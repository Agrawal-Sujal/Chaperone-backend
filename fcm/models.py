from django.db import models

class FCMToken(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=255)
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)