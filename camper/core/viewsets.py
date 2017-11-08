from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from camper.devices.models import Device
from camper.values.models import Value
from camper.events.models import Event


class StatsView(ViewSet):
    def list(self, request, format=None):
        return Response(dict(
            users=User.objects.count(),
            devices=Device.objects.count(),
            values=Value.objects.count(),
            events=Event.objects.count(),
        ))

