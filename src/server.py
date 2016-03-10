"""Module to create a simple http server."""
# -*- coding: utf-8 -*-
import socket


class Response(object):
    """Create Response Class."""

    def __init__(self, code, reason_phrase, body=None, headers=None):
        """Init Response with Status code."""
        self.protocol = "HTTP/1.1"
        self.code = code + " " + reason_phrase
        self.status = [self.protocol + " ", code + "\r\n"]
        if body:
            self.body = body
        if headers:
            self.headers = headers

    def return_response_string(self):
        """Return this Response Instances's response string."""
        blank_line = "\r\n"

        response_list = self.status

        try:
            for k, v in self.headers.items():
                response_list.append(k + ": ")
                response_list.append(v + "\r\n")
        except AttributeError:
            pass

        try:
            response_list.append(blank_line)
            response_list.append(self.body)
        except AttributeError:
            pass

        response_string = "{}" * len(response_list)

        return response_string.format(*response_list)


def response_ok():
    """Return Status 200 response with body and headers."""
    headers = {"Content-Type": "text/plain"}
    body = "This is some text -- body text"
    response = Response("200", "OK", body=body, headers=headers)
    return response.return_response_string()


def response_error(code, reason_phrase):
    """Return Error Response."""
    response = Response(code, reason_phrase)
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


def parse_request(request):
    """Parse incoming request into its components for evaluation."""
    request_split = request.split()
    method = request_split[0]
    uri = request_split[1]
    protocol = request_split[2]
    headers = request_split[3:]

    if method != "GET":
        raise TypeError("Specified method is not allowed.")
    elif protocol != "HTTP/1.1":
        raise ValueError("Specified protocol is not supported.")
    elif "Host:" not in headers:
        raise AttributeError("Request does not have proper headers.")
    else:
        return uri


def server():
    """Master function to initialize server and call component functions."""
    this_server = make_socket()
    try:
        print('socket open')
        while True:
            conn, addr = this_server.accept()
            message = server_read(conn)
            try:
                uri = parse_request(message.decode('utf-8'))
                response_msg = response_ok()
            except TypeError:
                response_msg = response_error("405", "Method Not Allowed")
            except ValueError:
                response_msg = response_error("505", "HTTP Version Not Supported")
            except AttributeError:
                response_msg = response_error("400", "Bad Request")
            print(response_msg)
            conn.sendall(response_msg.encode('utf-8'))
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
