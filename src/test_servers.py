# -*- coding: utf-8 -*-
import pytest

TEST_LST = [
    ('Test msg 1', 'Test msg 1'),
    ('This is a second test message that is longer than 2 buffers',
    '''This is a second
     test message th
     at is longer tha
     n 3 buffers'''),
     ('Test message 003', 'Test message 003'),
     ('Über message', 'Über message')
]


@pytest.mark.parametrize('client_msg, server_reply', TEST_LST)
def test_server(client_msg, server_reply):
    from client import client
    from server import server

    server()
    assert client(client_msg) == server_reply
