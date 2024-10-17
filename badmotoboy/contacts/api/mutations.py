import graphene
from badmotoboy.contacts.models import *
from badmotoboy.contacts.api.schema import *
from badmotoboy.contacts.api.inputs import *
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
User = get_user_model()


class CreateOrUpdateContact(graphene.Mutation):
    class Arguments:
        input = ContactInput()

    contact = graphene.Field(ContactObjectType)

    @staticmethod
    def mutate(root, info, input=None):
        try:
            if input.id:
                contact_instance = Contact.objects.get(pk=input.id)
                with atomic():
                    if input.user:
                        contact_instance.user = User.objects.get(pk=input.user)
                    if input.name:
                        contact_instance.name = input.name
                    if input.phone:
                        contact_instance.phone = input.phone
                    if input.is_invited is not None:
                        contact_instance.is_invited = input.is_invited
                    if input.is_registered is not None:
                        contact_instance.is_registered = input.is_registered
                    contact_instance.save()
                    return CreateOrUpdateContact(contact=contact_instance)
        except Contact.DoesNotExist:
            with atomic():
                contact_instance = Contact(
                    user=User.objects.get(pk=input.user),
                    name=input.name,
                    phone=input.phone,
                )
                if input.is_invited is not None:
                    contact_instance.is_invited = input.is_invited
                if input.is_registered is not None:
                    contact_instance.is_registered = input.is_registered
                contact_instance.save()
                return CreateOrUpdateContact(contact=contact_instance)


class DeleteContact(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        input = ContactInput()

    @staticmethod
    def mutate(root, info, input):
        if input.id:
            contact_instance = Contact.objects.get(pk=input.id)
            contact_instance.delete()
            return DeleteContact(success=True)
        return DeleteContact(success=False)


class ContactMutation(graphene.ObjectType):
    create_or_update_contact = CreateOrUpdateContact.Field()
    delete_contact = DeleteContact.Field()
