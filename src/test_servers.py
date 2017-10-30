# -*- coding: utf-8 -*-
"""Setup test functions.

To verify proper operation of server and client sockets.
"""
from __future__ import unicode_literals
import pytest

# Server side testing follows:


def test_parse_request_valid_input():
    """That that a valid request returns the URI."""
    from server import parse_request
    req = 'GET /path/to/index.html HTTP/1.1\r\nHost: /sample.txt\r\n\r\n'
    assert parse_request(req) == '/path/to/index.html'


def test_parse_request_with_method_not_allowed():
    """That that a request using a method other than GET raises an error."""
    from server import parse_request
    req = 'PUT /path/to/index.html HTTP/1.1\r\nHost: /sample.txt\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_parse_request_with_wrong_protocol():
    """That that request with protocol other than HTTP/1.1 raises an error."""
    from server import parse_request
    req = 'GET /path/to/index.html HTTP/1.0\r\nHost: /sample.txt\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_parse_request_missing_host_header():
    """That that request without a host header raises an error."""
    from server import parse_request
    req = 'GET /path/to/index.html HTTP/1.1\r\nHost /sample.txt\r\n\r\n'
    with pytest.raises(ValueError):
        parse_request(req)


def test_resolve_uri_works_with_txt():
    """Test proper response with txt file."""
    from server import resolve_uri
    assert resolve_uri('/sample.txt')[0] == 'text/plain'


def test_resolve_uri_works_with_png():
    """Test proper URI resolution with PNG file."""
    from server import resolve_uri
    assert resolve_uri('/images/sample_1.png')[0] == 'image/png'


def test_resolve_uri_works_with_jpg():
    """Test proper URI resolution with jpeg file."""
    from server import resolve_uri
    assert resolve_uri('/images/JPEG_example.jpg')[0] == 'image/jpeg'


def test_resolve_uri_works_with_html():
    """Test proper URI resolution with html file."""
    from server import resolve_uri
    assert resolve_uri('/a_web_page.html')[0] == 'text/html'


def test_resolve_uri_works_with_python_file():
    """Test proper URI resolution with .py file."""
    from server import resolve_uri
    assert resolve_uri('/make_time.py')[0] == 'text/plain'


def test_resolve_uri_works_with_directory():
    """Test proper URI resolution with directory input."""
    from server import resolve_uri
    assert resolve_uri('/images')[0] == 'text/directory'


def test_resolve_uri_raises_415():
    """Test unsupported file type raises 415 error."""
    from server import resolve_uri
    with pytest.raises(TypeError):
        resolve_uri('/images/sample.bmp')


def test_resolve_uri_raises_404():
    """Test bad directory raises 404 error."""
    from server import resolve_uri
    with pytest.raises(IOError):
        resolve_uri('/your_mom')


# Client side testing follows:


def test_client_sending_valid_request():
    """Test 200 ok response when client sends proper request."""
    from client import client
    assert client('sample.txt')[:15] == 'HTTP/1.1 200 OK'


def test_client_receives_requested_content_type():
    """Test that client gets content of the requested type."""
    from client import client
    assert 'Content-Type: text/plain' in client('sample.txt')


def test_client_receives_directory_list():
    """Test that client gets a listing of directory contents."""
    from client import client
    dir_list = ('<li>JPEG_example.jpg</li>')
    assert dir_list in client('images/')


def test_client_receives_png_image():
    """Test that client gets back requested image type."""
    from client import client
    assert 'Content-Type: image/png' in client('images/sample_1.png')


def test_client_receives_jpeg_image():
    """Test that client gets back requested image type."""
    from client import client
    assert 'Content-Type: image/jpeg' in client('images/JPEG_example.jpg')


def test_client_requests_unsupported_file_type():
    """."""
    from client import client
    assert client('images/sample.bmp') == "HTTP/1.1 415 Unsupported Media Type"


def test_client_requests_file_not_in_directory():
    """."""
    from client import client
    assert client('your_mom') == "HTTP/1.1 404 File or Directory Not Found"


# def test_client_sending_request_with_wrong_formatting():
#     """Test that wrongly formatted request gets 400 error."""
#     from client import client
#     req = 'GET /sample.txt HTTP/1.1\r\nHost: /sample.txt\r\n'
#     assert client(req) == "HTTP/1.1 400 Improperly Formed Request"


# def test_client_sending_request_with_wrong_http_version():
#     """Test that wrongly formatted request, gets 505 error."""
#     from client import client
#     req = 'GET /sample.txt HTTP/1.0\r\nHost: /sample.txt\r\n\r\n'
#     assert client(req) == "HTTP/1.1 505 HTTP Version Not Supported"


# def test_client_sending_proper_host_header_error():
#     """Test that request with missing host header gets 400 error."""
#     from client import client
#     req = 'GET /sample.txt HTTP/1.0\r\nHost- /sample.txt\r\n\r\n'
#     assert client(req) == "HTTP/1.1 400 Missing host header."
