import socket


class Client:
    def __init__(self):
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip, port):
        self._s.connect((ip, port))

    def send(self, message):
        self._s.send(message.encode())

    def receive(self):
        return self._s.recv(2048).decode()

    def close(self):
        self._s.close()
