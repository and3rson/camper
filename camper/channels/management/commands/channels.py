from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from camper.channels.models import redis
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import select
import json


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Channel server started')
        server = Server('0.0.0.0', 9080)
        self.event_listener = EventListener(server)
        self.event_listener.start()
        server.main()


class Server(object):
    READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR

    def __init__(self, host, port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(10)

        self.clients = {}

        self.fd_socket_map = {
            self.socket.fileno(): self.socket
        }
        self.poller = select.poll()

    def main(self):
        self.poller.register(self.socket, Server.READ_ONLY)
        while True:
            print('Polling, known sockets:', len(self.fd_socket_map))
            for fd, flag in self.poller.poll(1000):
                conn = self.fd_socket_map[fd]
                if flag & (select.POLLIN | select.POLLPRI):
                    if conn is self.socket:
                        # New conn
                        new_conn, info = self.socket.accept()
                        new_conn.setblocking(0)
                        self.fd_socket_map[new_conn.fileno()] = new_conn
                        self.poller.register(new_conn, Server.READ_ONLY)
                    else:
                        data = conn.recv(1024)
                        if not data:
                            print('Got nothing from client, dropping')
                            self.poller.unregister(conn)
                            conn.close()
                            del self.fd_socket_map[fd]
                        else:
                            print('Got', data)
                            self.handle(conn, data)
                elif flag & select.POLLHUP:
                    print('Received HUP from client, dropping')
                    self.poller.unregister(conn)
                    conn.close()

    def handle(self, conn, data):
        if conn not in self.clients:
            self.clients[conn] = Client(conn)
        client = self.clients[conn]

        data = data.decode('utf-8')
        cmd, _, data = data.strip().partition(' ')
        cmd = cmd.upper()
        if cmd == 'AUTH':
            if client.is_authorized:
                conn.send(b'ER Already authorized.\r\n')
            else:
                username, _, password = data.strip().partition(':')
                user = authenticate(username=username, password=password)
                if user:
                    client.user = user
                    conn.send(b'OK\r\n')
                else:
                    conn.send(b'ER Bad credentials.\r\n')
        else:
            if client.is_authorized:
                print('Cmd', cmd, 'from user', client.user, 'with data', data)
                conn.send(b'OK\r\n')
            else:
                conn.send(b'ER Please AUTH first.\r\n')

    def iter_clients(self):
        for client in self.clients.values():
            yield client

    def broadcast(self, username, command, data):
        for client in self.iter_clients():
            if client.check_username(username):
                client.send('{} {}\r\n'.format(command, data).encode('UTF-8'))


class Client(object):
    def __init__(self, conn):
        self.conn = conn
        self.user = None

    @property
    def is_authorized(self):
        return self.user is not None

    def check_username(self, username):
        return self.is_authorized and self.user.username == username

    def send(self, data):
        self.conn.send(data)


class EventListener(Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        pubsub = redis.pubsub()
        pubsub.subscribe('output')

        for event in pubsub.listen():
            if event['type'] == 'message':
                print('Got event', event)
                data = json.loads(event['data'])
                self.server.broadcast(data['username'], 'DATA', data['channel'] + ' ' + data['data'])

