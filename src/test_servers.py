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


def test_response_status():
    """Test responses for presence of status code and protocol."""
    from server import response_ok
    from server import response_error
    good_resp_msg = response_ok()
    bad_resp_msg = response_error("500", "some text")

    good_split = good_resp_msg.split(" ")
    bad_split = bad_resp_msg.split(" ")

    assert good_split[1][:1:] == "2"
    assert bad_split[1][:1:] == "5"
    assert good_split[0] == "HTTP/1.1"
    assert bad_split[0] == "HTTP/1.1"


def test_response_headers():
    """Test responses for proper headers."""
    from server import response_ok
    from server import response_error
    good_resp_msg = response_ok()
    bad_resp_msg = response_error("500", "some text")

    good_split = good_resp_msg.split("\r\n")
    bad_split = bad_resp_msg.split("\r\n")

    assert good_split[1][:7:] == "Content"
    assert good_split[1][12] == ":"
    assert bad_split[1] == ""


def test_response_break():
    """Test responses for blank break line between header and body."""
    from server import response_ok
    from server import response_error
    good_resp_msg = response_ok()
    bad_resp_msg = response_error("500", "some text")

    good_split = good_resp_msg.split("\r\n\r\n")
    bad_split = bad_resp_msg.split("\r\n\r\n")

    assert len(good_split) == 2
    assert len(bad_split) == 2


def test_parser():
    """Test the parser function."""
    request_str = b"""
    GET /favicon.ico HTTP/1.1\r\n
    Host: 111.1.1.1:4000\r\n
    """

    request_split = request_str.split()
    method = request_split[0]
    uri = request_split[1]
    protocol = request_split[2]
    host = request_split[3]

    assert method == b"GET"
    assert uri == b"/favicon.ico"
    assert protocol == b"HTTP/1.1"
    assert host == b"Host:"


def test_parse_req():
    """Test parser for proper capture of URI."""
    from server import parse_request
    request_str = """
    GET /favicon.ico HTTP/1.1\r\n
    Host: 111.1.1.1:4000\r\n
    """
    request_split = request_str.split()
    uri = request_split[1]
    assert parse_request(request_str) == uri


def test_parse_req_method():
    """Test that parser raises TypeError on improper request method."""
    from server import parse_request
    request_str = """
    POST /favicon.ico HTTP/1.1\r\n
    Host: 111.1.1.1:4000\r\n
    """
    with pytest.raises(TypeError):
        parse_request(request_str)


def test_parse_req_protocol():
    """Test that parser raises ValueError on improper HTTP protocol."""
    from server import parse_request
    request_str = """
    GET /favicon.ico HTTP/1.0\r\n
    Host: 111.1.1.1:4000\r\n
    """
    with pytest.raises(ValueError):
        parse_request(request_str)


def test_parse_req_host():
    """Test that parser raises AttributeError when Host header is missing."""
    from server import parse_request
    request_str = """
    GET /favicon.ico HTTP/1.1\r\n
    Something\r\n
    """
    with pytest.raises(AttributeError):
        parse_request(request_str)
