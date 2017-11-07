from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from camper.controls.models import Control
from django.db.models import Prefetch


class ThingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ThingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return models.Thing.objects.prefetch_related(
            'input_channels', 'values', Prefetch(
                'controls', Control.objects.select_subclasses()
            )
        ).filter(owner=self.request.user)

