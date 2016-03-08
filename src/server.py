# -*- coding: utf-8 -*-
import socket


def make_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    return server


def socket_listen(server):
    server.listen(1)
    conn, addr = server.accept()
    return conn, addr


def server_read(conn):
    buffer_length = 16
    message_complete = False
    echo_message = ""

    while not message_complete:
        part = conn.recv(buffer_length)
        echo_message += part.decode('utf8')
        if len(part) < buffer_length:
            break

    return echo_message


def server():
    try:
        this_server = make_socket()
        print('socket open')
        while True:
            conn, addr = socket_listen(this_server)
            echo_message = server_read(conn)
            print(echo_message)
            conn.sendall(echo_message.encode('utf-8'))
            conn.close()

    except KeyboardInterrupt:
        print('connection closing')
        conn.close()
        print('Socket closing')
        this_server.close()
