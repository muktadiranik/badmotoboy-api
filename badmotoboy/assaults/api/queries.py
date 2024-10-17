import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from badmotoboy.assaults.api.schema import AssaultEventObjectType
from badmotoboy.assaults.models import AssaultEvent
from badmotoboy.assaults.tasks import update_user


class AssaultEventQuery(graphene.ObjectType):
    assaults = DjangoFilterConnectionField(AssaultEventObjectType)

    @login_required
    def resolve_assaults(self, info, latitude_longitude=None, **kwargs):
        if latitude_longitude:
            latitude, longitude = latitude_longitude.split(",")
            update_user.delay(info.context.user.email, latitude, longitude)
        return AssaultEvent.objects.all()


assault_schema_query = graphene.Schema(query=AssaultEventQuery)
