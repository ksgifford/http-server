# -*- coding: utf-8 -*-
import socket


def make_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    return server


def socket_listen():
    server.listen(1)
    conn, addr = server.accept()
    return conn, addr


def server_read():
    buffer_length = 1024
    message_complete = False
    echo_message = ""

    while not message_complete:
    part = conn.recv(buffer_length)
    echo_message += part
    if len(part) < buffer_length:
        break

    return echo_message


def start_socket()
    server = make_socket()
    conn, addr = socket_listen()
    echo_message = server_read()
    conn.sendall(echo_message.encode('utf-8'))
