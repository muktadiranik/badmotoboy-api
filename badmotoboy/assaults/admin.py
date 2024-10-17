from django.contrib import admin
from badmotoboy.assaults.models import AssaultEvent


class AssaultEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude',)


admin.site.register(AssaultEvent, AssaultEventAdmin)
