from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers


class ValueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ValueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return models.Value.objects.all().filter(owner=self.request.user)

