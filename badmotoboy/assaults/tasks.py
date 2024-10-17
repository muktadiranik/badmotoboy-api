from firebase_admin.messaging import *
from fcm_django.models import FCMDevice
import math
from celery import shared_task
from django.db.transaction import atomic
from django.contrib.auth import get_user_model
User = get_user_model()


@shared_task(bind=True)
def update_user(self, email, latitude, longitude):
    try:
        with atomic():
            user = User.objects.get(email=email)
            user.latitude = latitude
            user.longitude = longitude
            user.save()
    except:
        pass


@shared_task(bind=True)
def send_message_to_fcm_devices(self,
                                email,
                                name,
                                center_longitude_radians,
                                center_latitude_radians,
                                radius,
                                assault_event_instance_latitude,
                                assault_event_instance_longitude,
                                assault_id,
                                assault_link):
    try:
        users = User.objects.exclude(email=email)
        for i in users:
            if i.latitude is None:
                continue
            with atomic():
                point_longitude = i.longitude
                point_latitude = i.latitude
                point_longitude_radians = math.radians(point_longitude)
                point_latitude_radians = math.radians(point_latitude)
                dx = center_longitude_radians - point_longitude_radians
                dy = center_latitude_radians - point_latitude_radians
                distance = math.sqrt(dx**2 + dy**2) * 6371000
                if distance <= radius:
                    try:
                        device = FCMDevice.objects.filter(user=i).first()
                        message = Message(
                            token=device.registration_id,
                            notification=Notification(
                                title='BadMotoBoy',
                                body=name + ' fired an Assault!'
                            ),
                            data={
                                "latitude": str(assault_event_instance_latitude),
                                "longitude": str(assault_event_instance_longitude),
                                "link": str(assault_link),
                                "assaultId": str(assault_id)
                            },
                            android=AndroidConfig(
                                priority='high',
                                notification=AndroidNotification(
                                    default_vibrate_timings=True
                                )
                            )
                        )
                        device.send_message(message)
                    except:
                        pass
    except:
        pass
