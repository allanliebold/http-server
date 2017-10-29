# -*- coding: utf-8 -*-
"""Create a server socket to recieve a message from a client.

And send back a response.
"""

from __future__ import unicode_literals
import sys
import os
import socket


def server():  # pragma: no cover
    """Build a server to rece/ive from client and respond."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 6666)
    server.bind(address)
    server.listen(1)
    listening = True
    try:
        while listening:
            conn, addr = server.accept()
            buffer_length = 8
            message_complete = False
            whole_msg = ''
            while not message_complete:
                part = conn.recv(buffer_length)
                whole_msg += part.decode('utf-8')
                if whole_msg[-3:] == '@@@':
                    break
            print(whole_msg[:-3])
            req = whole_msg[:-3]
            sys.stdout.write(req)
            try:
                parsed_uri_info = resolve_uri(parse_request(req))
                conn.sendall(response_ok(parsed_uri_info))
            except (IOError, TypeError, ValueError) as message:
                conn.sendall(response_error(message.args[0][0],
                                            message.args[0][1]))
            conn.close()
    except KeyboardInterrupt:
        conn.close()
        server.close()
        print('Server closed')
        sys.exit()


def parse_request(request):
    """Parse Response function.

    If passed a well-formed HTTP/1.1 GET request, return the request URI.
    Otherwise, raise the appropriate exception.
    """
    request_by_crlf = request.split("\r\n")
    if request_by_crlf[1][:5] != "Host:":
        raise ValueError([400, "Missing host header."])
    elif request[-2:] != "\r\n" or request.count("\r\n") < 3:
        raise ValueError([400, "Improperly Formed Request"])

    request_list = request.split()

    if request_list[0] != 'GET':
        raise ValueError([405, "Method Not Allowed"])

    if request_list[2][:8] != 'HTTP/1.1':
        raise ValueError([505, "HTTP Version Not Supported"])

    """If no errors arise, return the request URI."""
    return request_list[1]


def resolve_uri(uri_string):
    """Resolve URI passed in from a well-formed GET request.

    Check if file or directory exists. If it does, return the type and content.
    Otherwise, raise an error.
    """
    response_content = ['', '']
    if uri_string[-1] == '/':
        uri_string = uri_string[:-1]
    file_path = os.path.dirname(os.path.realpath(__file__)) + '/webroot'\
        + uri_string
    uri_list = os.path.split(file_path)
    if os.path.isdir(file_path):
        response_content[0] = 'text/directory'
        dir_contents = os.listdir(file_path)
        response_content[1] = '<ul>'
        for file in dir_contents:
            response_content[1] += '<li>{}</li>'.format(file)
        response_content[1] += '</ul>'
    elif uri_list[1] in os.listdir(uri_list[0]):
        if uri_list[1] and '.' in uri_list[1]:
            file_type = uri_list[1].split('.')[1]
            if file_type == 'txt' or file_type == 'py':
                response_content[0] = 'text/plain'
            elif file_type == 'jpg':
                response_content[0] = 'image/jpeg'
            elif file_type == 'png':
                response_content[0] = 'image/png'
            elif file_type == 'html':
                response_content[0] = 'text/html'
            else:
                raise TypeError([415, "Unsupported Media Type"])
            fp = open(file_path, 'rb')
            response_content[1] = fp.read()
            fp.close()
    else:
        raise IOError([404, "File or Directory Not Found"])

    return response_content


def response_ok(potato):
    """Return a well-formed HTTP 200 response.

    Accepts resolved URI with content type and body to add to the response.
    """
    resp_head = 'HTTP/1.1 200 OK\r\n'
    return '{}Content-Type: {}\r\n\r\n{}\r\n'.format(resp_head,
                                                     potato[0],
                                                     potato[1]).encode("utf-8")


def response_error(status, reason):
    """Return a well-formed error for the status passed."""
    return "HTTP/1.1 {} {}".format(status, reason).encode('utf-8')

if __name__ == "__main__":  # pragma: no cover
    """Run server from the command line."""
    server()
