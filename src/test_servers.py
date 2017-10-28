# -*- coding: utf-8 -*-
"""Setup test functions.

To verify proper operation of server and client sockets.
"""
from __future__ import unicode_literals
import pytest


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
    assert client(req) == response_ok().decode('utf-8')


def test_client_sending_request_with_wrong_method():
    """Test error message when client sends wrong method request."""
    from client import client
    req = 'PUT /path/to/index.html HTTP/1.1\r\nHost: www.mysite1.com:80\r\n\r\n'
    assert client(req) == "HTTP/1.1 405 Method Not Allowed"


def test_client_sending_request_with_wrong_formatting():
    """Test that when client sends wrongly formatted request, gets 400 error."""
    from client import client
    req = 'GET /path/to/index.html HTTP/1.1\r\nHost: www.mysite1.com:80\r\n'
    assert client(req) == "HTTP/1.1 400 Improperly Formed Request"


def test_client_sending_request_with_wrong_http_version():
    """Test that when client sends wrongly formatted request, gets 505 error."""
    from client import client
    req = 'GET /path/to/index.html HTTP/1.0\r\nHost: www.mysite1.com:80\r\n\r\n'
    assert client(req) == "HTTP/1.1 505 HTTP Version Not Supported"


def test_client_sending_proper_host_header_error():
    from client import client
    req = 'GET /path/to/index.html HTTP/1.0\r\nHost- www.mysite1.com:80\r\n\r\n'
    assert client(req) == "HTTP/1.1 400 Missing host header."