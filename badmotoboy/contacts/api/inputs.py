import graphene


class ContactInput(graphene.InputObjectType):
    id = graphene.ID()
    user_id = graphene.ID()
    name = graphene.String()
    phone = graphene.String()
    is_invited = graphene.Boolean()
    is_registered = graphene.Boolean()
