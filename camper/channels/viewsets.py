from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from . import models
from . import serializers
from camper.core.parsers import DataQueryParser


class InputChannelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InputChannelSerializer
    queryset = models.InputChannel.objects.all()

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


# class OutputChannelViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.OutputChannelSerializer
#     queryset = models.OutputChannel.objects.all()

