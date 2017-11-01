from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import APIException
from rest_framework.filters import BaseFilterBackend
from django.utils.dateparse import parse_datetime
from coreapi import Field
from . import models
from . import serializers
from camper.core.parsers import DataQueryParser


class InputChannelViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InputChannelSerializer
    queryset = models.InputChannel.objects.all()

    @detail_route(methods=['POST'], serializer_class=serializers.NotifySerializer, parser_classes=[DataQueryParser, JSONParser])
    def notify(self, request, pk):
        channel = self.get_object()
        serializer = serializers.NotifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        values = channel.notify(serializer.validated_data['data'])
        # except models.ValueUpdateException as e:
        #     raise APIException(detail='Value "{}" failed to update, please check json_path of related values. Reason was: "{}"'.format(
        #         e.value,
        #         e.reason
        #     ))
        return Response(serializers.ValueSerializer(
            instance=values,
            many=True,
            context=dict(request=request)
        ).data)


class ValueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ValueSerializer
    queryset = models.Value.objects.all()


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    class DateFilterBackend(BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            since = parse_datetime(request.query_params.get('since', ''))
            if since:
                print('Filtering since', since)
                queryset = queryset.filter(date_created__gt=since)
            else:
                print('FAIL')
            queryset = queryset[:10]
            return queryset

        def get_schema_fields(self, view):
            return [
                Field(
                    name='since',
                    required=False,
                    location='query',
                    description='Minimum datetime.'
                )
            ]

    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.order_by('-date_created')
    filter_backends = [DateFilterBackend]


# class OutputChannelViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.OutputChannelSerializer
#     queryset = models.OutputChannel.objects.all()

