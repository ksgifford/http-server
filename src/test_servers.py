"""Tests to ensure that our server is properly echoing the client."""
# _*_ coding: utf-8 _*_

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
    good_resp_obj, good_resp_msg = response_ok()
    bad_resp_obj, bad_resp_msg = response_error()

    good_split = good_resp_msg.split(" ")
    bad_split = bad_resp_msg.split(" ")

    assert good_split[1][:1:] == "2"
    assert bad_split[1][:1:] == "5"
    assert good_split[0] == "HTTP/1.1"
    assert good_split[0] == good_resp_obj.protocol
    assert bad_split[0] == "HTTP/1.1"
    assert bad_split[0] == bad_resp_obj.protocol


def test_response_headers():
    """Test responses for proper headers."""
    from server import response_ok
    from server import response_error
    good_resp_obj, good_resp_msg = response_ok()
    bad_resp_obj, bad_resp_msg = response_error()

    good_split = good_resp_msg.split("\r\n")
    bad_split = bad_resp_msg.split("\r\n")

    assert good_split[1][:7:] == "Content"
    assert good_split[1][12] == ":"
    assert bad_split[1] == ""


def test_response_break():
    """Test responses for blank break line between header and body."""
    from server import response_ok
    from server import response_error
    good_resp_obj, good_resp_msg = response_ok()
    bad_resp_obj, bad_resp_msg = response_error()

    good_split = good_resp_msg.split("\r\n\r\n")
    bad_split = bad_resp_msg.split("\r\n\r\n")

    assert len(good_split) == 2
    assert len(bad_split) == 2
