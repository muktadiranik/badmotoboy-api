import graphene
from graphene_django import DjangoObjectType
from badmotoboy.users.models import Gender, UserProfile
from badmotoboy.users.api.filters import *
from django.contrib.auth import get_user_model
User = get_user_model()


class UserObjectType(DjangoObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = User
        fields = "__all__"
        filterset_class = UserFilter
        interfaces = (graphene.relay.Node,)


class GenderObjectType(DjangoObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = Gender
        fields = "__all__"
        filterset_class = GenderFilter
        interfaces = (graphene.relay.Node,)


class UserProfileObjectType(DjangoObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
        filterset_class = UserProfileFilter
        interfaces = (graphene.relay.Node,)
