# -*- coding: utf-8 -*-
"""Setup test functions.

To verify proper operation of server and client sockets.
"""
from __future__ import unicode_literals


def test_client():
    """Test the client socket setup."""
    from client import client
    assert client("Send this") == "Send this"


def test_messages_shorter_than_one_buffer():
    """Test if message is shorter than buffer, still works."""
    from client import client
    assert client('hi') == "hi"


def test_messages_longer_than_one_buffer_length():
    """Test that messages longer than one buffer still work."""
    long_message = "This is a super long message that is way longer than \
        the default buffer length"
    from client import client
    assert client(long_message) == long_message


def test_messages_exact_multiplier_of_buffer():
    """Test messages that are exact buffer size multiples work."""
    from client import client
    assert client("12345678") == "12345678"


def test_messages_1():
    """Test that when sending "1" we get back "1"."""
    from client import client
    assert client("1") == "1"


def test_messages_2():
    """Test that when sending "12" we get back "12"."""
    from client import client
    assert client("12") == "12"


def test_messages_3():
    """Test that when sending "123" we get back "123"."""
    from client import client
    assert client("123") == "123"


def test_messages_6():
    """Test that when sending "123456" we get back "123456"."""
    from client import client
    assert client("123456") == "123456"


def test_messages_7():
    """Test that when sending "1234567" we get back "1234567"."""
    from client import client
    assert client("1234567") == "1234567"


def test_messages_with_non_ascii_chars():
    """Test that non ascii chars are returned as sent."""
    from client import client
    assert client(u"Œš™- word yo!") == u"Œš™- word yo!"
