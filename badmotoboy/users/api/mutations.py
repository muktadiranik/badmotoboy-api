import graphene
import graphql_jwt
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import create_refresh_token, get_token
from graphql import GraphQLError
from badmotoboy.users.api.schema import *
from badmotoboy.users.api.inputs import *
from badmotoboy.users.models import UserProfile, Gender
User = get_user_model()


class CreateOrUpdateUser(graphene.Mutation):
    user = graphene.Field(UserObjectType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        input = UserInput(required=True)

    def mutate(self, info, input):
        try:
            user = User.objects.get(uid=input.uid)
            if user:
                with atomic():
                    if input.email:
                        user.email = input.email
                    if input.username:
                        user.username = input.username
                    if input.name:
                        user.name = input.name
                    if input.password:
                        user.set_password(input.password)
                    user.save()
                    token = get_token(user)
                    refresh_token = create_refresh_token(user)
                    user_profile_instance = UserProfile.objects.filter(user_id=user.id).first()
                    if input.avatar_url:
                        user_profile_instance.avatar_url = input.avatar_url
                    if input.display_name:
                        user_profile_instance.display_name = input.display_name
                    user_profile_instance.save()
                    return CreateOrUpdateUser(
                        user=user,
                        token=token,
                        refresh_token=refresh_token
                    )
        except:
            if User.objects.filter(email=input.email):
                return GraphQLError("The Email has already been taken")
            with atomic():
                user = User(uid=input.uid)
                if input.email:
                    user.email = input.email
                if input.password:
                    user.set_password(input.password)
                if input.name:
                    user.name = input.name
                if input.username:
                    user.username = input.username
                user.save()
                token = get_token(user)
                refresh_token = create_refresh_token(user)
                user_profile_instance = UserProfile.objects.create(user=user)
                if input.avatar_url:
                    user_profile_instance.avatar_url = input.avatar_url
                if input.display_name:
                    user_profile_instance.display_name = input.display_name
                user_profile_instance.save()
                return CreateOrUpdateUser(
                    user=user,
                    token=token,
                    refresh_token=refresh_token
                )


class CreateOrUpdateUserProfile(graphene.Mutation):
    user_profile = graphene.Field(UserProfileObjectType)

    class Arguments:
        input = UserProfileInput()

    def mutate(self, info, input):
        try:
            user_profile_instance = UserProfile.objects.get(user=User.objects.get(uid=input.uid))
            if user_profile_instance:
                if input.display_name:
                    user_profile_instance.display_name = input.display_name
                if input.age:
                    user_profile_instance.age = input.age
                if input.gender:
                    user_profile_instance.gender = Gender.objects.get(pk=input.gender)
                if input.city:
                    user_profile_instance.city = input.city
                if input.avatar_url:
                    user_profile_instance.avatar_url = input.avatar_url
                if input.avatar:
                    user_profile_instance.avatar = input.avatar
                user_profile_instance.save()
                return CreateOrUpdateUserProfile(user_profile=user_profile_instance)
        except:
            return CreateOrUpdateUserProfile(user_profile=None)


class UpdateUserLocation(graphene.Mutation):
    user = graphene.Field(UserObjectType)

    class Arguments:
        input = UserInput()

    def mutate(self, info, input):
        try:
            user = User.objects.get(uid=input.uid)
            if user:
                user.latitude = input.latitude
                user.longitude = input.longitude
                user.save()
                return UpdateUserLocation(user=user)
        except:
            return UpdateUserLocation(user=None)


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_or_update_user = CreateOrUpdateUser.Field()
    create_or_update_user_profile = CreateOrUpdateUserProfile.Field()
    update_user_location = UpdateUserLocation.Field()


user_schema_mutation = graphene.Schema(mutation=AuthMutation)
