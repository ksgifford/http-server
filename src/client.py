# -*- coding: utf-8 -*-
import sys
import socket
from server import server


def client(message):
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client_socket = socket.socket(*stream_info[:3])

    client_socket.connect(stream_info[-1])

    client_socket.sendall(message.encode('utf8'))

    buffer_msg = ''
    buffer_length = 16
    echo_complete = False
    while not echo_complete:
        part = client_socket.recv(buffer_length)
        buffer_msg += part.decode('utf8')
        if len(part) < buffer_length:
            break
        print(buffer_msg)

    client_socket.close()


if __name__ == "__main__":
    server()
    client(str(sys.argv[1]))
