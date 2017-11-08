from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers


class ControlViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ControlSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Control.objects.all().filter(
            owner=self.request.user
        ).select_subclasses()


class SwitchControlViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SwitchControlSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return models.SwitchControl.objects.all().filter(
            owner=self.request.user
        )


class RangeControlViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RangeControlSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return models.RangeControl.objects.all().filter(
            owner=self.request.user
        )

