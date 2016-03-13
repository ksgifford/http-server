"""Module to create a simple http server."""
# -*- coding: utf-8 -*-
import io
import os
import mimetypes


BUFF_LENGTH = 1024


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

        encoded_response = "{}{}\r\n".format(response, str_headers)
        encoded_response = encoded_response.encode("utf-8")
        if self.body:
            if type(self.body) is not bytes:
                self.body = self.body.encode("utf-8")
            encoded_response = encoded_response + self.body
        return encoded_response


def build_directory_tree(path):
    """Build HTML response body for directory listings and return mimetype."""
    body = "<!DOCTYPE html><html><body>"
    mimetype = "text/html"
    for dir_name, sub_dir_list, file_list in os.walk(path):
        body += "<h3>Directory: {}</h3>".format(dir_name.split("webroot")[-1])
        body += "<ul>"
        for fname in file_list:
            body += "<li>{} </li>".format(fname)
        body += "</ul>"
    body += "</body></html>"
    return body, mimetype


def resolve_uri(uri):
    """Resolve path to resource on local file system and get contents."""
    homedir = os.path.dirname(__file__)
    webroot = "webroot"

    uri = uri.lstrip("/")
    path = os.path.join(homedir, webroot, uri)

    mimetype = mimetypes.guess_type(path)[0]

    if not mimetype:
        if not os.path.isdir(path):
            raise IOError
        body, mimetype = build_directory_tree(path)
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


def server_read(conn):
    """Read incoming client message and create echo message to client."""
    message_complete = False
    message = []

    while not message_complete:
        part = conn.recv(BUFF_LENGTH)
        message.append(part)
        if len(part) < BUFF_LENGTH:
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


def assemble_response(request):
    """Assemble response message from parsed client request."""
    uri = parse_request(request.decode("utf-8"))
    resolved_uri = resolve_uri(uri)
    response_msg = response_ok(*resolved_uri)
    return response_msg


def manage_client(request, conn):
    """Handle incoming client requests and response messages."""
    try:
        response_msg = assemble_response(request)
    except RequestError as ex:
        response_msg = response_error(*ex.args)
    except IOError:
        response_msg = response_error(404, "File Not Found")
    except OSError:
        response_msg = response_error(404, "File Not Found")
    finally:
        try:
            conn.sendall(response_msg)
        except NameError:
            pass


def server(conn, address):
    """Master function to initialize server and call component functions."""
    print("Client Connection Open")
    while True:
        request = server_read(conn)
        if request:
            print(request)
            manage_client(request, conn)


if __name__ == "__main__":
    server()
