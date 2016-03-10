"""Module to create a simple http server."""
# -*- coding: utf-8 -*-
import socket


class Response(object):
    """Create Response Class."""

    def __init__(self, code, headers=None, body=None):
        """Init Response with Status code."""
        self.protocol = "HTTP/1.1 "
        self.code = code
        self.status = [self.protocol, code + "\n"]
        if headers: self.headers = headers
        self.body = body

    def return_response_string(self):
        """Return this Response Instances's response string."""
        blank_line = "\r\n"

        response_list = self.status

        if self.headers:
            for k, v in self.headers.items():
                response_list.append(k + ": ")
                response_list.append(v + "\r\n")

        response_list.append(blank_line)
        response_list.append(self.body)

        response_string = "{}" * len(response_list)

        return response_string.format(*response_list)


def response_ok():
    """Return Status 200 response with body and headers."""
    headers = {"Content-Type": "text/plain"}
    body = "This is some text -- body text"
    response = Response("200 OK", headers=headers, body=body)
    return response.return_response_string()


def response_error():
    """Return Error Response."""
    response = Response("500 INTERNAL SERVER ERROR")
    return response.return_response_string()


def make_socket():
    """Build a socket for the server, set attributes, and bind address."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    server.listen(1)
    return server


def server_read(conn):
    """Read incoming client message and create echo message to client."""
    buffer_length = 16
    message_complete = False
    message = []

    while not message_complete:
        part = conn.recv(buffer_length)
        message.append(part)
        if len(part) < buffer_length:
            break

    return b"".join(message)


def server():
    """Master function to initialize server and call component functions."""
    this_server = make_socket()
    try:
        print('socket open')
        while True:
            conn, addr = this_server.accept()
            message = server_read(conn)
            print(message.decode('utf-8'))
            response = response_ok()
            print(response)
            conn.sendall(response.encode('utf-8'))
            conn.close()

    except KeyboardInterrupt:
        try:
            conn.close()
        except NameError:
            pass

    finally:
        print('Socket closing')
        this_server.close()

if __name__ == "__main__":
    server()
