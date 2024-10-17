from django.db import models
from auditlog.registry import auditlog
from django_quill.fields import QuillField


class PrivacyPolicy(models.Model):
    content = QuillField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id.__str__()

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policies'


auditlog.register(PrivacyPolicy)


class TermsAndConditions(models.Model):
    content = QuillField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id.__str__()

    class Meta:
        verbose_name = 'Terms and Conditions'
        verbose_name_plural = 'Terms and Conditions'


auditlog.register(TermsAndConditions)


class ContactUs(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'


auditlog.register(ContactUs)
