from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Avg
from datetime import timedelta
from . import models
from . import serializers


class ValueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ValueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return models.Value.objects.all().filter(owner=self.request.user)

    @detail_route(methods=['GET'], serializer_class=serializers.ValueLogSerializer)
    def log(self, request, pk):
        value = self.get_object()
        return Response(
            serializers.ValueLogSerializer(
                many=True,
                instance=value.logs.all().order_by('-date_created'),
                context=dict(request=request)
            ).data
        )

    @detail_route(methods=['GET'])
    def stats(self, request, pk):
        value = self.get_object()
        resolution = request.query_params.get('resolution', 'hours')
        count = request.query_params.get('count', 12)
        samples = []
        max_avg = None

        for diff in range(count, 0, -1):
            # delta_start = timedelta(**{resolution: diff})
            # delta_end = timedelta(**{resolution: diff - 1})
            datetime_start = now() - timedelta(**{resolution: diff})
            datetime_end = datetime_start + timedelta(**{resolution: 1})
            logs = value.logs.filter(
                date_created__gt=datetime_start,
                date_created__lte=datetime_end
            ).values('data')  # .aggregate(Avg('data'))['data_avg']
            if len(logs):
                avg = sum(log['data'] for log in logs) / len(logs)
            else:
                avg = 0
            if max_avg is None or avg > max_avg:
                max_avg = avg
            samples.append(
                dict(
                    delta=-diff,
                    avg=avg
                )
            )
        return Response(dict(
            max_avg=max_avg,
            count=count,
            resolution=resolution,
            samples=samples
        ))

