from socketserver import TCPServer, BaseRequestHandler, ThreadingMixIn
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from camper.core.utils import redis
from threading import Thread
import json
import traceback
import threading


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Channel server started')
        self.event_listener = EventListener()
        self.event_listener.start()
        chan_server = ChannelServer(('0.0.0.0', 9080), ChannelHandler)
        chan_server.serve_forever()


class ChannelServer(ThreadingMixIn, TCPServer):
    pass


class ChannelHandler(BaseRequestHandler):
    clients = []

    def handle(self):
        ChannelHandler.clients.append(self)
        self.user = None

        while True:
            try:
                self.process_data()
            except Exception as e:
                print('Got error on client, dropping. Error was:', str(e))
                ChannelHandler.clients.remove(self)
                return

    def process_data(self):
        print('Handling thread', threading.current_thread())
        data = self.request.recv(1024).decode('utf-8')
        if not data:
            raise Exception('Received empty response')
        cmd, _, data = data.strip().partition(' ')
        cmd = cmd.upper()
        if cmd == 'AUTH':
            if self.is_authorized:
                self.send(b'ER Already authorized.\r\n')
            else:
                username, _, password = data.strip().partition(':')
                user = authenticate(username=username, password=password)
                if user:
                    self.user = user
                    self.send(b'OK\r\n')
                else:
                    self.send(b'ER Bad credentials.\r\n')
        else:
            if self.is_authorized:
                print('Cmd', cmd, 'from user', self.user, 'with data', data)
                self.send(b'OK\r\n')
            else:
                self.send(b'ER Please AUTH first.\r\n')

    @property
    def is_authorized(self):
        return self.user is not None

    def check_username(self, username):
        return self.is_authorized and self.user.username == username

    def send(self, data):
        try:
            self.request.sendall(data)
        except Exception as e:
            print('Got an error while trying to send data:')
            traceback.print_exc()
            print('Ignoring above exception.')

    @classmethod
    def iter_clients(cls):
        for client in cls.clients:
            yield client

    @classmethod
    def broadcast(cls, username, command, data):
        for client in cls.iter_clients():
            if client.check_username(username):
                client.request.sendall('{} {}\r\n'.format(command, data).encode('UTF-8'))


class EventListener(Thread):
    def run(self):
        pubsub = redis.pubsub()
        pubsub.subscribe('output')

        for event in pubsub.listen():
            if event['type'] == 'message':
                # print('Got event', event)
                data = json.loads(event['data'])
                ChannelHandler.broadcast(data['username'], 'DATA', data['value'] + ' ' + json.dumps(data['data']))

