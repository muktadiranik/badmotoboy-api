import graphene
from graphene_django import DjangoObjectType
from badmotoboy.contacts.models import Contact
from badmotoboy.contacts.api.filters import ContactFilter


class ContactObjectType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Contact
        fields = '__all__'
        filterset_class = ContactFilter
        interfaces = (graphene.relay.Node,)
