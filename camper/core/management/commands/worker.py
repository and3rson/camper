from django.core.management.base import BaseCommand
from camper.things.models import Thing
from camper.channels.models import Event
from time import sleep


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Worker started')
        while True:
            for thing in Thing.objects.all().prefetch_related('values'):
                alive_state = thing.get_is_alive()
                if alive_state != thing.is_alive:
                    print('Thing "{}" changed is_alive state to {}'.format(thing, alive_state))
                    thing.is_alive = alive_state
                    thing.save()
                    Event.objects.create(
                        type='thing-alive-state-changed',
                        object=thing,
                        data=alive_state
                    )
            sleep(1)

