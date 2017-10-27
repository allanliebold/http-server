# -*- coding: utf-8 -*-
"""Setup test functions.

To verify proper operation of server and client sockets.
"""
from __future__ import unicode_literals
import pytest


# def test_client():
#     """Test the client socket setup."""
#     from client import client
#     from server import response_ok
#     assert client("Send this") == response_ok()


# def test_messages_shorter_than_one_buffer():
#     """Test if message is shorter than buffer, still works."""
#     from client import client
#     from server import response_ok
#     assert client('hi') == response_ok()


# def test_messages_longer_than_one_buffer_length():
#     """Test that messages longer than one buffer still work."""
#     long_message = "This is a super long message that is way longer than \
#         the default buffer length"
#     from client import client
#     from server import response_ok
#     assert client(long_message) == response_ok()


# def test_messages_exact_multiplier_of_buffer():
#     """Test messages that are exact buffer size multiples work."""
#     from client import client
#     from server import response_ok
#     assert client("12345678") == response_ok()


# def test_messages_1():
#     """Test that when sending "1" we get back a 200 OK response."""
#     from client import client
#     from server import response_ok
#     assert client("1") == response_ok()


# def test_messages_2():
#     """Test that when sending "12" we get back a 200 OK response."""
#     from client import client
#     from server import response_ok
#     assert client("12") == response_ok()


# def test_messages_3():
#     """Test that when sending "123" we get back a 200 OK response."""
#     from client import client
#     from server import response_ok
#     assert client("123") == response_ok()


# def test_messages_6():
#     """Test that when sending "123456" we get back a 200 OK response."""
#     from client import client
#     from server import response_ok
#     assert client("123456") == response_ok()


# def test_messages_7():
#     """Test that when sending "1234567" we get back a 200 OK response."""
#     from client import client
#     from server import response_ok
#     assert client("1234567") == response_ok()


# def test_messages_with_non_ascii_chars():
#     """Test that non ascii chars are sent and get a 200 OK response."""
#     from client import client
#     from server import response_ok
#     assert client(u"Œš™- word yo!") == response_ok()


def test_parse_request_valid_input():
    """That that a valid request returns the URI."""
    from server import parse_request
    req = 'GET /path/to/index.html HTTP/1.1\r\nHost: www.mysite1.com:80\r\n\r\n'
    assert parse_request(req) == '/path/to/index.html'


def test_parse_request_with_method_not_allowed():
    """That that a request using a method other than GET raises an error."""
    from server import parse_request
    req = 'PUT /path/to/index.html HTTP/1.1\r\nHost: www.mysite1.com:80\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_parse_request_with_wrong_protocol():
    """That that request with protocol other than HTTP/1.1 raises an error."""
    from server import parse_request
    req = 'GET /path/to/index.html HTTP/1.0\r\nHost: www.mysite1.com:80\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_parse_request_missing_host_header():
    """That that request without a host header raises an error."""
    from server import parse_request
    req = 'GET /path/to/index.html HTTP/1.1\r\nHost www.mysite1.com:80\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_client_sending_valid_request():
    """Test 200 ok response when client sends proper request."""
    from client import client
    from server import response_ok
    req = 'GET /path/to/index.html HTTP/1.1\r\nHost: www.mysite1.com:80\r\n\r\n'
    assert client(req) == response_ok()


def test_client_sending_request_with_wrong_method():
    """Test error message when client sends wrong method request."""
    from client import client
    req = 'PUT /path/to/index.html HTTP/1.1\r\nHost: www.mysite1.com:80\r\n\r\n'
    assert client(req) == b'HTTP/1.1 405 Method Not Allowed'
