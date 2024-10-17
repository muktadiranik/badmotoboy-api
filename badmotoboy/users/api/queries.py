import graphene
from graphene_django import DjangoConnectionField
from django.contrib.auth import get_user_model
from badmotoboy.users.models import Gender, UserProfile
from badmotoboy.users.api.schema import *
User = get_user_model()


class AuthQuery(graphene.ObjectType):
    users = DjangoConnectionField(UserObjectType)
    genders = DjangoConnectionField(GenderObjectType)
    user_profiles = DjangoConnectionField(UserProfileObjectType)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_genders(self, info, **kwargs):
        return Gender.objects.all()

    def resolve_user_profiles(self, info, **kwargs):
        return UserProfile.objects.all()


user_schema_query = graphene.Schema(query=AuthQuery)
