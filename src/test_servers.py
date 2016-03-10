"""Tests to ensure that our server is properly echoing the client."""
# NOTE: Server must be started manually before running Pytest.
# _*_ coding: utf-8 _*_
import pytest

TEST_LST = [
    ('Test msg 1', 'Test msg 1'),
    ('Test message 003', 'Test message 003'),
    ('The quick brown fox jumped over the lazy brown dog',
     'The quick brown fox jumped over the lazy brown dog'),
    (u'Über message', u'Über message')
]


# @pytest.mark.parametrize('client_msg, server_reply', TEST_LST)
# def test_server(client_msg, server_reply):
#     """Test that server returns client message."""
#     from client import client

#     assert client(client_msg) == server_reply


def test_response_ok():
    from server import server
    response = response_ok()
    split = response.split(" ")
    assert split[2][:3:] == b"200"




def test_response_error():
    assert response_error() ==

