# stockdata/models.py
from django.db import models

class FyersToken(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    token_type = models.CharField(max_length=50, null=True, blank=True)
    expires_in = models.IntegerField(null=True, blank=True)
    scope = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
