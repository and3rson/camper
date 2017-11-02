from django.core.management.base import BaseCommand
from camper.values.models import Value
from time import sleep


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Worker started')
        while True:
            try:
                values = list(Value.objects.all())
            except:
                print('DB not ready yet')
            else:
                for value in values:
                    value.check_alive_state()
            sleep(1)

