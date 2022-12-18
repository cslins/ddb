import sys
import socket
from threading import Thread
import pickle
import test


class Server:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket_server.bind((host, port))

        self.socket_server.listen(100)

        print(f"Listening at {host}:{port}")

        while True:
            socket_client, address = self.socket_server.accept()
            print(f"Connection from {address} has been established!")

            process = Thread(target=self.processing, args=(socket_client,))

            process.start()

    def processing(self, curr_socket_client: socket.socket):

        data_recv = curr_socket_client.recv(__bufsize=4096)
        data = pickle.loads(data_recv)

        # TODO insert processing logic here
        print(data)

        reply = "kek"
        reply_encoded = reply.encode("utf-8")
        curr_socket_client.send(reply_encoded)


# host: str = socket.gethostname()
# port: int = sys.argv[1]
#
# socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# socket_server.bind((host, port))
#
# socket_server.listen(100)
#
# print(f"Listening at {host}:{port}")
#
#
# def processing(curr_socket_client: socket.socket):
#
#     # TODO insert processing logic here
#
#     data = "data"
#     response = data.encode("utf-8")
#     curr_socket_client.send(response)
#
#
# while True:
#
#     socket_client, address = socket_server.accept()
#     print(f"Connection from {address} has been established!")
#
#     process = Thread(target=processing, args=(socket_client,))
#
#     process.start()
