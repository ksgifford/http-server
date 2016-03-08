# -*- coding: utf-8 -*-
import sys
import socket


def client(message):
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client_socket = socket.socket(*stream_info[:3])

    client_socket.connect(stream_info[-1])

    client_socket.sendall(message.encode('utf8'))

    buffer_length = 16
    echo_complete = False
    while not echo_complete:
        part = client_socket.recv(buffer_length)
        print(part.decode('utf8'))
        if len(part) < buffer_length:
            break

    client_socket.close()


if __name__ == "__main__":
    client(str(sys.argv[1]))
