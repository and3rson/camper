from rest_framework import parsers
from rest_framework.exceptions import ValidationError


class DataQueryParser(parsers.BaseParser):
    media_type = 'text/x-data-query'

    def parse(self, stream, media_type=None, parser_context=None):
        raw = stream.read().decode('utf-8')
        print('Received payload:', raw)
        data = dict()
        for key, _, value in [pair.partition('=') for pair in raw.split('&')]:
            try:
                if float(value) == int(value):
                    value = int(value)
                else:
                    value = float(value)
            except:
                pass
            node = data
            path = key.split('.')
            try:
                for i, part in enumerate(path):
                    if part not in node:
                        node[part] = dict()
                    if i < len(path) - 1:
                        node = node[part]
                node[part] = value
            except TypeError:
                raise ValidationError(detail='Malformed data structure in payload: attempt to assign to scalar value as to dictionary.')
        return data

