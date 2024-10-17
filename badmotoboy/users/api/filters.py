from django_filters import *
from badmotoboy.users.models import UserProfile, Gender
from django.contrib.auth import get_user_model
User = get_user_model()


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = {
            "uid": ["exact"],
            "username": ["exact"],
            "email": ["exact"],
            "id": ["exact"],
        }


class GenderFilter(FilterSet):
    class Meta:
        model = Gender
        fields = {
            "name": ["exact"],
            "id": ["exact"],
        }


class UserProfileFilter(FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            "user": ["exact"],
            "id": ["exact"],
        }
