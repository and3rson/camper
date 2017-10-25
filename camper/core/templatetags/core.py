from json import dumps
from django.template import Library
from django.utils.html import mark_safe

register = Library()


@register.filter()
def json(value):
    return mark_safe(dumps(value, indent=4))

