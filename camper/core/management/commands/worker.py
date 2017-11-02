from django.core.management.base import BaseCommand
from camper.values.models import Value
from time import sleep


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Worker started')
        while True:
            for value in Value.objects.all():
                value.check_alive_state()
            sleep(1)

