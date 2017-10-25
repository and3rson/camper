from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from . import models
from . import serializers


class InputChannelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InputChannelSerializer
    queryset = models.InputChannel.objects.all()

    @detail_route(methods=['POST'], serializer_class=serializers.NotifySerializer)
    def notify(self, request, pk):
        channel = self.get_object()
        serializer = serializers.NotifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = channel.notify(serializer.validated_data['data'])
        return Response(serializers.ValueSerializer(
            instance=values,
            many=True,
            context=dict(request=request)
        ).data)


class ValueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ValueSerializer
    queryset = models.Value.objects.all()


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.order_by('-date_created')


# class OutputChannelViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.OutputChannelSerializer
#     queryset = models.OutputChannel.objects.all()

