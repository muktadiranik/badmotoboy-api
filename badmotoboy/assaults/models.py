from django.db import models
from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
User = get_user_model()


class AssaultEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    latitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)
    longitude = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


auditlog.register(AssaultEvent)
