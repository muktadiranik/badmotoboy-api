from django.db import models
from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    is_invited = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


auditlog.register(Contact)
