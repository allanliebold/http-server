"""Setup test functions.

To verify proper operation of server and client sockets.

"""


import sys
import socket
from server import server



# def test_server():
#     """Test the server socket setup."""
#     assert True


def test_client():
    """Test the client socket setup."""
    from client import client
    assert client("Send this") == "Server received message"


def test_messages_shorter_than_one_buffer():
    from client import client
    assert client('hi') == "Server received message"

def test_messages_longer_than_one_buffer_length():
    from client import client
    assert client("This is a super long message that is way longer than the default buffer length") == "Server received message"

def test_messages_exact_multiplier_of_buffer():
    from client import client
    assert client("1234567 1234567 1234567 12345678") == "Server received message"

# def test_messages_with_non_ascii_chars():
#     from server import server
#     from client import client
#     assert True
