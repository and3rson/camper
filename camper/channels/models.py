from django.db import models


class Channel(models.Model):
    class Meta:
        abstract = True

    id = models.SlugField(null=False, blank=False, primary_key=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Channel {}'.format(
            self.id
        )

    __repr__ = __str__


class InputChannel(Channel):
    def notify(self, data):
        values = []

        for thing in self.things.all():
            thing.notify(data)

        return values


class OutputChannel(Channel):
    destination_url = models.URLField(null=False, blank=False)


# class Transformer(models.Model):
#     TEMPLATE_HEADER = '{% load core %}\n'

#     id = models.UUIDField(null=False, blank=False, default=uuid.uuid1, primary_key=True, editable=False)
#     script = models.TextField(null=False, blank=False, default='{{ data|json }}')

#     def feed(self, data):
#         template = Template(Transformer.TEMPLATE_HEADER + self.script)
#         transformed = template.render(Context(dict(data=data)))
#         return json.loads(transformed)

