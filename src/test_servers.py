"""Setup test functions.

To verify proper operation of server and client sockets.

"""


def test_client():
    """Test the client socket setup."""
    from client import client
    assert client("Send this") == "Send this"


def test_messages_shorter_than_one_buffer():
    from client import client
    assert client('hi') == "hi"


def test_messages_longer_than_one_buffer_length():
    from client import client
    assert client("This is a super long message that is way longer than the default buffer length") == "This is a super long message that is way longer than the default buffer length"


def test_messages_exact_multiplier_of_buffer():
    from client import client
    assert client("123456") == "123456"

def test_messages_1():
    from client import client
    assert client("1") == "1"

def test_messages_2():
    from client import client
    assert client("12") == "12"

def test_messages_3():
    from client import client
    assert client("123") == "123"

def test_messages_6():
    from client import client
    assert client("123456") == "123456"

def test_messages_7():
    from client import client
    assert client("1234567") == "1234567"

def test_messages_8():
    from client import client
    assert client("12345678") == "12345678"

# def test_messages_with_non_ascii_chars():
#     from client import client
#     assert True
