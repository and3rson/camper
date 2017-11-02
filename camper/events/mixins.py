from .models import Event


class EventEmitter(object):
    def emit(self, type, **kwargs):
        Event.objects.create(
            type=type,
            object=self,
            data=kwargs
        )

