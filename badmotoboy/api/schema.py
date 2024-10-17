import graphene
from badmotoboy.users.api.queries import *
from badmotoboy.users.api.mutations import *
from badmotoboy.assaults.api.queries import *
from badmotoboy.assaults.api.mutations import *
from badmotoboy.contacts.api.queries import *
from badmotoboy.contacts.api.mutations import *
from badmotoboy.users.api.queries import *

class Query(AuthQuery,
            AssaultEventQuery,
            ContactQuery,
            graphene.ObjectType):

    pass


class Mutation(AuthMutation,
               AssaultEventMutation,
               ContactMutation,
               graphene.ObjectType):
    pass
