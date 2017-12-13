import requests


class Backend(object):
    def notify(self, config, value):
        raise NotImplementedError()


class TelegramBackend(Backend):
    name = 'Telegram'

    def notify(self, config, value):
        requests.post(
            'https://api.telegram.org/bot{token}/sendMessage'.format(**config),
            json=dict(
                text='{} @ {} changed to {}{}'.format(
                    value.name,
                    value.device.name,
                    value.data,
                    (' @' + config.get('mention')) if config.get('mention') else ''
                ),
                chat_id=config.get('chat_id')
            )
        )


BACKENDS = {
    'telegram': TelegramBackend
}

