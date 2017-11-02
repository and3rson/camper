from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from camper.things.models import Thing
from camper.channels.models import InputChannel
from camper.values.models import Value
from camper.events.models import Event


class StatsView(ViewSet):
    def list(self, request, format=None):
        return Response(dict(
            users=User.objects.count(),
            things=Thing.objects.count(),
            input_channels=InputChannel.objects.count(),
            values=Value.objects.count(),
            events=Event.objects.count(),
        ))

