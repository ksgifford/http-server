"""Module to create a simple http server."""
# -*- coding: utf-8 -*-
import socket
import io
import os
import mimetypes

ADDRESS = ("0.0.0.0", 5000)


class RequestError(BaseException):
    """Class for creating new exceptions for HTTP requests."""

    def __init__(self, code, reason):
        """Inherit from BaseException class."""
        super(RequestError, self).__init__(code, reason)


class Response(object):
    """Create Response Class."""

    def __init__(self, code, reason_phrase, body=None, headers=None):
        """Init Response with Status code."""
        self.protocol = "HTTP/1.1"
        self.code = "{} {}".format(code, reason_phrase)
        self.body = body
        self.headers = headers

    def return_response_string(self):
        """Return this Response Instance's response string."""
        response = "{} {}\r\n".format(self.protocol, self.code)
        str_headers = ""
        if self.headers:
            for k, v in self.headers.items():
                str_headers += "{}: {}\r\n".format(k, v)

        encoded_response = "{}{}\r\n".format(response, str_headers).encode("utf-8")
        if self.body:
            if type(self.body) is not bytes:
                self.body = self.body.encode("utf-8")
            encoded_response = encoded_response + self.body
        return encoded_response


def resolve_uri(uri):
    """Resolve path to resource on local file system and get contents."""
    homedir = os.getcwd()
    webroot = "webroot"

    uri = uri.lstrip("/")
    print("URI: " + uri)
    if not uri:
        path = os.path.join(homedir, webroot)
    else:
        path = os.path.join(homedir, webroot, uri)
    print("File Path: " + path)
    body = "<!DOCTYPE html><html><body>"

    mimetype = mimetypes.guess_type(path)[0]

    if not mimetype:
        if not os.path.isdir(path):
            raise IOError
        mimetype = "text/html"
        for dir_name, sub_dir_list, file_list in os.walk(path):
            body += "<h3>Directory: {}</h3>".format(dir_name.split("webroot")[-1])
            body += "<ul>"
            for fname in file_list:
                body += "<li>{} </li>".format(fname)
            body += "</ul>"
        body += "</body></html>"
        print(body)
    else:
        f = io.open(path, "rb")
        body = f.read()
        f.close()
    return (body, mimetype)


def response_ok(body, content_type):
    """Return Status 200 response with body and headers."""
    headers = {
        "Content-Length": len(body),
        "Content-Type": content_type,
    }
    response = Response(200, "OK", body=body, headers=headers)

    return response.return_response_string()


def response_error(code, reason_phrase):
    """Return Error Response."""
    body = """<!DOCTYPE html><html><body><h2>Uh oh...\n{} {}
            </h2></body></html""".format(code, reason_phrase).encode("utf-8")
    header = {"Content-Type": "text/html"}
    response = Response(code, reason_phrase, body, header)
    return response.return_response_string()


def make_socket():
    """Build a socket for the server, set attributes, and bind address."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.bind(ADDRESS)
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
    print("Protocol: " + protocol)
    headers = request_split[3]

    if method != "GET":
        raise RequestError(405, "Method Not Allowed")
    elif protocol != "HTTP/1.1":
        raise RequestError(505, "HTTP Version Not Supported")
    elif "Host:" not in headers:
        raise RequestError(400, "Bad Request")
    else:
        return uri


def server():
    """Master function to initialize server and call component functions."""
    this_server = make_socket()
    try:
        print("socket open")
        while True:
            conn, addr = this_server.accept()
            message = server_read(conn)
            response_msg = "TEST"
            if message:
                print(message)
                try:
                    uri = parse_request(message.decode("utf-8"))
                    resolved_uri = resolve_uri(uri)
                    response_msg = response_ok(resolved_uri[0], resolved_uri[1])
                except RequestError as ex:
                    response_msg = response_error(*ex.args)
                except IOError:
                    response_msg = response_error(404, "File Not Found")
                finally:
                    # print(u"The requested URI is: " + uri)
                    print(response_msg)
                    conn.sendall(response_msg)
                    conn.close()

    except KeyboardInterrupt:
        try:
            conn.close()
        except NameError:
            pass

    finally:
        print("Socket closing")
        this_server.close()

if __name__ == "__main__":
    server()
