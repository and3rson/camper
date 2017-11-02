from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers


class ThingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ThingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return models.Thing.objects.prefetch_related('input_channels', 'values').filter(owner=self.request.user)

