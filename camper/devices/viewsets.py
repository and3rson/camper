from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from . import models
from . import serializers
from camper.values.models import Value
from camper.controls.models import Control
from django.db.models import Prefetch
from camper.core.parsers import DataQueryParser, JPEGParser
import logging

logger = logging.getLogger('internal')


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DeviceSerializer
    permission_classes = [IsAuthenticated]

    @detail_route(
        methods=['POST'],
        serializer_class=serializers.NotifySerializer,
        parser_classes=[DataQueryParser, JSONParser, JPEGParser]
    )
    def notify(self, request, pk):
        device = self.get_object()
        serializer = serializers.NotifySerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.exception('Bad notification for device %s: %s', pk, e)
            raise
        device.notify(serializer.validated_data['data'])
        return Response(serializer.data)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return models.Device.objects.prefetch_related(
            Prefetch(
                'values', Value.objects.order_by('name')
            ),
            Prefetch(
                'values__controls', Control.objects.order_by('name').select_subclasses()
            )
        ).filter(owner=self.request.user).order_by('name')

