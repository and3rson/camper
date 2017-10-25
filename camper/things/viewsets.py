from rest_framework import viewsets
from . import models
from . import serializers


class ThingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ThingSerializer
    queryset = models.Thing.objects.all()

