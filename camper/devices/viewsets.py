from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from . import models
from . import serializers
from camper.controls.models import Control
from django.db.models import Prefetch
from camper.core.parsers import DataQueryParser


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DeviceSerializer
    permission_classes = [IsAuthenticated]

    @detail_route(
        methods=['POST'],
        serializer_class=serializers.NotifySerializer,
        parser_classes=[DataQueryParser, JSONParser]
    )
    def notify(self, request, pk):
        device = self.get_object()
        serializer = serializers.NotifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device.notify(serializer.validated_data['data'])
        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return models.Device.objects.prefetch_related(
            'values',
            Prefetch(
                'values__controls', Control.objects.select_subclasses()
            )
        ).filter(owner=self.request.user)

