from rest_framework import viewsets
from . import models
from . import serializers


class ValueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ValueSerializer
    queryset = models.Value.objects.all()

