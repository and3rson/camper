from socketserver import TCPServer, BaseRequestHandler, ThreadingMixIn
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from camper.core.utils import redis
from camper.devices.models import Device
from threading import Thread
import time
import json
import logging
import logging.config

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('internal')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logger.info('Channel server started')
        chan_server = ChannelServer(('0.0.0.0', 9080), ChannelHandler)
        self.event_listener = EventListener(chan_server)
        self.event_listener.start()
        pinger = Pinger(chan_server)
        pinger.start()
        chan_server.serve_forever()


class ChannelServer(ThreadingMixIn, TCPServer):
    clients = []

    def iter_clients(self):
        for client in self.clients:
            yield client


class ChannelHandler(BaseRequestHandler):
    HELLO_MSG = (
        'Hi there!',
        '',
        'Here\'s what you can send:',
        ' - "AUTH <username>:<password>" - authorize before you can do anything.',
        ' - "DVID <device_id>" - to start receiving notifications from some device.',
        '',
        'Here\'s what you are going to receive:',
        ' - "INFO <info>" - usage information (sent only at the very start, right now.)',
        ' - "OKAY" - your last operation was successful.',
        ' - "WARN <message>" - your last operation failed.',
        ' - "PING <timestamp>" - the server will ping you every 5 seconds.',
        ' - "DATA <device_id> <value_id> <json>" - some value has changed.',
        '',
        'Have fun!',
        '',
    )

    class ChannelError(Exception):
        pass

    def handle(self):
        self.user = None
        self.devices = []
        self.server.clients.append(self)

        for msg in ChannelHandler.HELLO_MSG:
            self.send('INFO {}\n'.format(msg))

        while True:
            try:
                self.process_data()
            except ChannelHandler.ChannelError as e:
                logger.warn('Dropping client %s: %s', self, str(e))
                self.server.clients.remove(self)
                return
            except Exception as e:
                logger.exception('Got exception on client %s, dropping.', self)
                self.server.clients.remove(self)
                return

    def process_data(self):
        try:
            data = self.request.recv(1024).decode('utf-8')
        except Exception as e:
            raise ChannelHandler.ChannelError('Failed to decode data as UTF-8')
        if not data:
            raise ChannelHandler.ChannelError('Received empty response')
        data = data.strip()
        logger.debug('Data from client %s: %s', self, data)
        cmd, _, data = data.partition(' ')
        cmd = cmd.upper()
        if cmd == 'AUTH':
            if self.is_authorized:
                self.send(b'WARN Already authorized.\n')
                return
            username, _, password = data.strip().partition(':')
            user = authenticate(username=username, password=password)
            if user:
                self.user = user
                self.send(b'OKAY\n')
            else:
                self.send(b'WARN Bad credentials.\n')
        elif cmd == 'DVID':
            if not self.is_authorized:
                self.send(b'WARN Please AUTH first.\n')
                return
            device = Device.objects.filter(id=data.strip(), owner=self.user).first()
            if not device:
                self.send(b'WARN Unknown device ID.\n')
                return
            self.devices.append(device)
            self.send(b'OKAY\n')
        else:
            self.send(b'WARN Unknown command.\n')

    @property
    def is_authorized(self):
        return self.user is not None

    def has_device(self, device_id):
        return self.is_authorized and device_id in [device.id for device in self.devices]

    def check_username(self, username):
        return self.is_authorized and self.user.username == username

    def send(self, data):
        if isinstance(data, str):
            data = data.encode('UTF-8')
        try:
            self.request.sendall(data)
        except Exception as e:
            logger.exception('Got an error while trying to send data.')

    def __repr__(self):
        return '<ChannelHandler user={}>'.format(self.user)

    __str__ = __repr__


class EventListener(Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        pubsub = redis.pubsub()
        pubsub.subscribe('output')

        for event in pubsub.listen():
            if event['type'] == 'message':
                self.process_event(json.loads(event['data']))

    def process_event(self, event_data):
        for client in self.server.iter_clients():
            if not client.has_device(event_data['device_id']):
                continue
            payload = json.dumps(event_data['data'])
            logger.info(
                'Sending update to %s: device = %s, value_id = %s, data = %s',
                client.user,
                event_data['device_id'],
                event_data['value_id'],
                payload
            )
            client.send('DATA {} {} {}\n'.format(
                event_data['device_id'],
                event_data['value_id'],
                payload
            ))


class Pinger(Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        while True:
            for client in self.server.iter_clients():
                client.send('PING {}\n'.format(str(int(time.time() * 1000000))))
            time.sleep(5)

