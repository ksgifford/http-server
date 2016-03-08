"""Module to create a simple echo server."""
# -*- coding: utf-8 -*-
import socket


def make_socket():
    """Build a socket for the server, set attributes, and bind address."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    return server


def socket_listen(server):
    """Listen for a client and accept connection."""
    server.listen(1)
    conn, addr = server.accept()
    return conn, addr


def server_read(conn):
    """Read incoming client message and create echo message to client."""
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
    """Master function to initialize server and call component functions."""
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
