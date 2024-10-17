import graphene
from .schema import ContactObjectType
from graphene_django.filter import DjangoFilterConnectionField
from badmotoboy.contacts.models import Contact


class ContactQuery(graphene.ObjectType):

    contacts = DjangoFilterConnectionField(ContactObjectType)

    def resolve_contacts(self, info, **kwargs):
        return Contact.objects.all()


contact_schema_query = graphene.Schema(query=ContactQuery)
