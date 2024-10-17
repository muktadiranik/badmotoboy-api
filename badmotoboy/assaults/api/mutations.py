import math
import requests
import graphene
import environ
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from badmotoboy.assaults.api.inputs import *
from badmotoboy.assaults.api.schema import *
from badmotoboy.assaults.tasks import *
from badmotoboy.assaults.tasks import *
from fcm_django.models import FCMDevice
from firebase_admin.messaging import *
User = get_user_model()
env = environ.Env()


class CreateAssaultEvent(graphene.Mutation):
    class Arguments:

        input = CreateAssaultEventInput()

    assault_event = graphene.Field(AssaultEventObjectType)

    @staticmethod
    @login_required
    def mutate(root, info, input=None):
        user = User.objects.get(pk=input.user)
        if user:
            with atomic():
                assault_event_instance = AssaultEvent(
                    user=user,
                    latitude=input.latitude,
                    longitude=input.longitude,
                )
                if input.address:
                    assault_event_instance.address = input.address
                assault_event_instance.save()
                link = f'https://badmotoboy.com/map?latitude={str(input.latitude)}&longitude={str(input.longitude)}&assaultId={assault_event_instance.id}'
                r = requests.post(
                    'https://firebasedynamiclinks.googleapis.com/v1/shortLinks',
                    params={
                        'key': env.str('FIREBASE_WEB_API_KEY')
                    },
                    json={
                        "dynamicLinkInfo": {
                            "domainUriPrefix": "https://badmotoboy.page.link",
                            "link": link,
                            "androidInfo": {
                                "androidPackageName": "com.badmotoboy"
                            },
                            # "iosInfo": {
                            #     "iosBundleId": "com.badmotoboy"
                            # }
                        }
                    },
                    headers={
                        'Content-Type': 'application/json'
                    }
                )
                res = r.json()
                short_link = res['shortLink']
                assault_event_instance.link = short_link
                assault_event_instance.save()
            center_longitude = assault_event_instance.longitude
            center_latitude = assault_event_instance.latitude
            center_longitude_radians = math.radians(center_longitude)
            center_latitude_radians = math.radians(center_latitude)
            radius = env.int("ASSAULT_RADIUS", 2000)
            send_message_to_fcm_devices.delay(
                info.context.user.email,
                user.name,
                center_longitude_radians,
                center_latitude_radians,
                radius,
                assault_event_instance.latitude,
                assault_event_instance.longitude,
                assault_event_instance.id,
                short_link)
            return CreateAssaultEvent(assault_event=assault_event_instance)
        else:
            return CreateAssaultEvent(assault_event=None)


class UpdateAssaultEvent(graphene.Mutation):
    class Arguments:
        input = UpdateAssaultEventInput(required=True)

    assault_event = graphene.Field(AssaultEventObjectType)

    @staticmethod
    def mutate(root, info, input=None):
        assault_event_instance = AssaultEvent.objects.get(pk=input.id)
        if assault_event_instance:
            if input.user:
                assault_event_instance.user = User.objects.get(pk=input.user)
            if input.latitude:
                assault_event_instance.latitude = input.latitude
            if input.longitude:
                assault_event_instance.longitude = input.longitude
            assault_event_instance.save()
            return UpdateAssaultEvent(assault_event=assault_event_instance)


class DeleteAssaultEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    assault_event = graphene.Field(AssaultEventObjectType)

    @staticmethod
    def mutate(root, info, id):
        assault_event_instance = AssaultEvent.objects.get(pk=id)
        assault_event_instance.delete()
        return None


class CreateFCMDevice(graphene.Mutation):
    class Arguments:
        input = FCMdeviceInput()

    fcm_device = graphene.Field(FCMDeviceObjectType)

    @staticmethod
    def mutate(root, info, input=None):
        try:
            if FCMDevice.objects.get(device_id=input.device_id, user_id=input.user):
                fcm_device_instance = FCMDevice.objects.get(
                    device_id=input.device_id, user_id=input.user)
                fcm_device_instance.name = input.name
                fcm_device_instance.registration_id = input.registration_id
                fcm_device_instance.active = input.active
                fcm_device_instance.type = input.type
                fcm_device_instance.save()
                return CreateFCMDevice(fcm_device=fcm_device_instance)
        except:
            fcm_device_instance, other = FCMDevice.objects.update_or_create(
                name=input.name,
                user=User.objects.get(id=input.user),
                registration_id=input.registration_id,
                type=input.type,
                device_id=input.device_id,
                active=input.active
            )
            return CreateFCMDevice(fcm_device=fcm_device_instance)


class AssaultEventMutation(graphene.ObjectType):
    create_assault_event = CreateAssaultEvent.Field()
    update_assault_event = UpdateAssaultEvent.Field()
    delete_assault_event = DeleteAssaultEvent.Field()
    create_fcm_device = CreateFCMDevice.Field()
