import socket
from _thread import start_new_thread


class Server(object):
    def __init__(self, port=0x7079):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((socket.gethostname(), self.port))
        self.socket.listen(5)
        self.handler = lambda addr, sock: True
        while True:
            (clientsocket, address) = self.socket.accept()
            start_new_thread(self.handler, (address, clientsocket))

    def use(self, handler):
        self.handler = handler
        return handler