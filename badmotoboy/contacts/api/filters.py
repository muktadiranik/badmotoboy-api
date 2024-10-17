from django_filters import *
from badmotoboy.contacts.models import Contact


class ContactFilter(FilterSet):
    class Meta:
        model = Contact
        fields = {
            'id': ['exact'],
            "user_id": ['exact'],
            "name": ['icontains'],
            "phone": ['icontains'],
            "is_invited": ['exact'],
            "is_registered": ['exact'],
        }
