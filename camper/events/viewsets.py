from rest_framework.filters import BaseFilterBackend
from rest_framework import viewsets
from django.utils.dateparse import parse_datetime
from coreapi import Field
from . import models
from . import serializers


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    class DateFilterBackend(BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):
            since = parse_datetime(request.query_params.get('since', ''))
            if since:
                # print('Filtering since', since)
                queryset = queryset.filter(date_created__gt=since)
            # else:
            #     print('FAIL')
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

