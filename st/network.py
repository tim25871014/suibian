import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '127.0.0.1'
        self.port = 5557
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            #return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
    def load(self):
        try:
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)