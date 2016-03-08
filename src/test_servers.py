"""Tests to ensure that our server is properly echoing the client."""
# NOTE: Server must be started manually before running Pytest.
# -*- coding: utf-8 -*-
import pytest

TEST_LST = [
    ('Test msg 1', 'Test msg 1'),
    ('Test message 003', 'Test message 003'),
    ('The quick brown fox jumped over the lazy brown dog',
     'The quick brown fox jumped over the lazy brown dog'),
    ('Über message', 'Über message')
]


@pytest.mark.parametrize('client_msg, server_reply', TEST_LST)
def test_server(client_msg, server_reply):
    """Test that server returns client message."""
    from client import client

    assert client(client_msg) == server_reply
