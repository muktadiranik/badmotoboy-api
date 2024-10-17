import graphene


class CreateAssaultEventInput(graphene.InputObjectType):
    user = graphene.ID()
    latitude = graphene.Decimal()
    longitude = graphene.Decimal()
    address = graphene.String()


class UpdateAssaultEventInput(graphene.InputObjectType):
    id = graphene.ID()
    user = graphene.ID()
    latitude = graphene.Decimal()
    longitude = graphene.Decimal()


class FCMdeviceInput(graphene.InputObjectType):
    name = graphene.String()
    user = graphene.ID()
    registration_id = graphene.String()
    type = graphene.String()
    device_id = graphene.String()
    active = graphene.Boolean()
