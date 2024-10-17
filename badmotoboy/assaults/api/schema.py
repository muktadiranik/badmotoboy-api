import graphene
from graphene_django import DjangoObjectType
from fcm_django.models import FCMDevice
from badmotoboy.assaults.api.filters import AssaultEventFilter
from badmotoboy.assaults.models import AssaultEvent


class AssaultEventObjectType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = AssaultEvent
        fields = "__all__"
        filterset_class = AssaultEventFilter
        interfaces = (graphene.relay.Node,)


class FCMDeviceObjectType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = FCMDevice
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
