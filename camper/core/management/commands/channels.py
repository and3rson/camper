from socketserver import TCPServer, BaseRequestHandler, ThreadingMixIn
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from camper.core.utils import redis
from threading import Thread
import time
import json
import traceback
import threading


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Channel server started')
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

    def broadcast(self, username, command, data):
        for client in self.iter_clients():
            if username is None or client.check_username(username):
                client.request.sendall('{} {}\n'.format(command, data).encode('UTF-8'))


class ChannelHandler(BaseRequestHandler):
    def handle(self):
        print(self.server)
        self.server.clients.append(self)
        self.user = None

        while True:
            try:
                self.process_data()
            except Exception as e:
                print('Got error on client, dropping. Error was:', str(e))
                self.server.clients.remove(self)
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
                self.send(b'ER Already authorized.\n')
            else:
                username, _, password = data.strip().partition(':')
                user = authenticate(username=username, password=password)
                if user:
                    self.user = user
                    self.send(b'OK\n')
                else:
                    self.send(b'ER Bad credentials.\n')
        else:
            if self.is_authorized:
                print('Cmd', cmd, 'from user', self.user, 'with data', data)
                self.send(b'OK\n')
            else:
                self.send(b'ER Please AUTH first.\n')

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


class EventListener(Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        pubsub = redis.pubsub()
        pubsub.subscribe('output')

        for event in pubsub.listen():
            if event['type'] == 'message':
                # print('Got event', event)
                data = json.loads(event['data'])
                self.server.broadcast(data['username'], 'DATA', data['value'] + ' ' + json.dumps(data['data']))


class Pinger(Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        while True:
            self.server.broadcast(None, 'PING', str(int(time.time() * 1000000)))
            time.sleep(5)

