import sys
import socket
import pickle
import test

class Client:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port

        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket_client.connect((host, port))

    def __del__(self):
        self.socket_client.close()

    def send(self, data):
        message = pickle.dumps(data)
        self.socket_client.send(message)


host: str = sys.argv[1]
port: int = sys.argv[2]

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_client.connect((host, port))

# TODO insert processing logic here
