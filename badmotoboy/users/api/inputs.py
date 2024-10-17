import graphene
from django.contrib.auth import get_user_model
from graphene_file_upload.scalars import Upload
User = get_user_model()


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    uid = graphene.String()
    username = graphene.String()
    password = graphene.String()
    email = graphene.String()
    name = graphene.String()
    latitude = graphene.String()
    longitude = graphene.String()
    avatar_url = graphene.String()
    display_name = graphene.String()


class GenderInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class UserProfileInput(graphene.InputObjectType):
    id = graphene.ID()
    uid = graphene.String()
    display_name = graphene.String()
    age = graphene.Date()
    gender = graphene.ID()
    city = graphene.String()
    avatar_url = graphene.String()
    avatar = Upload()
