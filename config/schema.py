import graphene
from badmotoboy.api.schema import Query
from badmotoboy.api.schema import Mutation


schema = graphene.Schema(query=Query, mutation=Mutation)
