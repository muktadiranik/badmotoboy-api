from django.contrib import admin
from badmotoboy.common.models import *


class contactUsAdmin(admin.ModelAdmin):
    list_display = ('name',  'email', 'message', 'created_at')
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at',)


admin.site.register(PrivacyPolicy)
admin.site.register(TermsAndConditions)
admin.site.register(ContactUs, contactUsAdmin)
