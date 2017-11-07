from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from camper.core.parsers import DataQueryParser


class InputChannelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InputChannelSerializer
    permission_classes = [IsAuthenticated]

    @detail_route(
        methods=['POST'],
        serializer_class=serializers.NotifySerializer,
        parser_classes=[DataQueryParser, JSONParser]
    )
    def notify(self, request, pk):
        channel = self.get_object()
        serializer = serializers.NotifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = channel.notify(serializer.validated_data['data'])
        return Response(status=204)
        # return Response(serializers.ValueSerializer(
        #     instance=values,
        #     many=True,
        #     context=dict(request=request)
        # ).data)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return models.InputChannel.objects.all().filter(owner=self.request.user)


# class OutputChannelViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.OutputChannelSerializer
#     queryset = models.OutputChannel.objects.all()

