# -*- coding: utf-8 -*-
"""Setup test functions.

To verify proper operation of server and client sockets.
"""
from __future__ import unicode_literals


def test_client():
    """Test the client socket setup."""
    from client import client
    assert client("Send this") == "HTTP/1.1 200\nOK\r\n"


def test_messages_shorter_than_one_buffer():
    """Test if message is shorter than buffer, still works."""
    from client import client
    assert client('hi') == "HTTP/1.1 200\nOK\r\n"


def test_messages_longer_than_one_buffer_length():
    """Test that messages longer than one buffer still work."""
    long_message = "This is a super long message that is way longer than \
        the default buffer length"
    from client import client
    assert client(long_message) == "HTTP/1.1 200\nOK\r\n"


def test_messages_exact_multiplier_of_buffer():
    """Test messages that are exact buffer size multiples work."""
    from client import client
    assert client("12345678") == "HTTP/1.1 200\nOK\r\n"


def test_messages_1():
    """Test that when sending "1" we get back a 200 OK response."""
    from client import client
    assert client("1") == "HTTP/1.1 200\nOK\r\n"


def test_messages_2():
    """Test that when sending "12" we get back a 200 OK response."""
    from client import client
    assert client("12") == "HTTP/1.1 200\nOK\r\n"


def test_messages_3():
    """Test that when sending "123" we get back a 200 OK response."""
    from client import client
    assert client("123") == "HTTP/1.1 200\nOK\r\n"


def test_messages_6():
    """Test that when sending "123456" we get back a 200 OK response."""
    from client import client
    assert client("123456") == "HTTP/1.1 200\nOK\r\n"


def test_messages_7():
    """Test that when sending "1234567" we get back a 200 OK response."""
    from client import client
    assert client("1234567") == "HTTP/1.1 200\nOK\r\n"


def test_messages_with_non_ascii_chars():
    """Test that non ascii chars are sent and get a 200 OK response."""
    from client import client
    assert client(u"Œš™- word yo!") == "HTTP/1.1 200\nOK\r\n"
