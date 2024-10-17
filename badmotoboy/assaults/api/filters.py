from django_filters import *
from badmotoboy.assaults.models import *
import math
import environ
env = environ.Env()


class AssaultEventFilter(FilterSet):
    id = NumberFilter(field_name='id', lookup_expr='exact')
    user = NumberFilter(field_name="user", lookup_expr="exact")
    latitude_longitude = CharFilter(method="filter_latitude_longitude")

    class Meta:
        model = AssaultEvent
        fields = "__all__"

    def filter_latitude_longitude(self, queryset, name, value):
        latitude, longitude = value.split(",")
        center_longitude_radians = math.radians(float(longitude))
        center_latitude_radians = math.radians(float(latitude))
        radius = env.int("ASSAULT_RADIUS", 2000)
        assault_event_id_set = []
        for i in AssaultEvent.objects.all():
            point_longitude_radians = math.radians(i.longitude)
            point_latitude_radians = math.radians(i.latitude)
            dx = center_longitude_radians - point_longitude_radians
            dy = center_latitude_radians - point_latitude_radians
            distance = math.sqrt(dx**2 + dy**2) * 6371000
            if distance <= radius:
                assault_event_id_set.append(i.id)
        return AssaultEvent.objects.filter(id__in=assault_event_id_set)
