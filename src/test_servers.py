"""Tests to ensure that our server is properly echoing the client."""
# _*_ coding: utf-8 _*_
import pytest


TEST_LST = [
    ('Test msg 1', 'Test msg 1'),
    ('Test message 003', 'Test message 003'),
    ('The quick brown fox jumped over the lazy brown dog',
     'The quick brown fox jumped over the lazy brown dog'),
    (u'Über message', u'Über message')
]

TEST_REQUEST = """
    GET /sample.txt HTTP/1.1
    Host: 0.0.0.0:5000"""

TEST_REQUEST_404 = """
    GET /bad_file.txt HTTP/1.1
    Host: 0.0.0.0:5000"""


def test_request_protocol():
    """Test that server throws RequestError when protocol is incorrect."""
    from server import parse_request
    from server import RequestError
    test_str = """
    GET /favicon.ico HTTP/1.0\r\n
    Host: 111.1.1.1:4000\r\n"""

    with pytest.raises(RequestError):
        parse_request(test_str)


def test_request_method():
    """Test that server throws RequestError when method is not supported."""
    from server import parse_request
    from server import RequestError
    test_str = """
    POST /favicon.ico HTTP/1.1\r\n
    Host: 111.1.1.1:4000\r\n"""

    with pytest.raises(RequestError):
        parse_request(test_str)


def test_request_host():
    """Test that server throws IndexError when no headers are included."""
    from server import parse_request
    test_str = """
    GET /favicon.ico HTTP/1.1\r\n"""

    with pytest.raises(IndexError):
        parse_request(test_str)


def test_request_header_host():
    """Test that server throws RequestError when host header is not included."""
    from server import parse_request
    from server import RequestError
    test_str = """
    GET /favicon.ico HTTP/1.1\r\n
    Content-Type: text/html"""

    with pytest.raises(RequestError):
        parse_request(test_str)


def test_parse_request_uri():
    """Test that parse_request method properly extracts URI from request."""
    from server import parse_request
    test_str = """
    GET /favicon.ico HTTP/1.1\r\n
    Host: 111.1.1.1:4000\r\n"""

    assert parse_request(test_str) == "/favicon.ico"


def test_response_constructor_proto():
    """Test that Response class constructor uses proper protocol."""
    from server import Response
    test_resp = Response(200, "OK")
    assert test_resp.protocol == "HTTP/1.1"


def test_response_constructor_code():
    """Test that Response class constructor returns proper status code."""
    from server import Response
    test_resp = Response(200, "OK")
    assert test_resp.code == "200 OK"


def test_response_constructor_not():
    """Test that constructor does not return body/headers w/o input."""
    from server import Response
    test_resp = Response(200, "OK")
    assert not test_resp.body
    assert not test_resp.headers
