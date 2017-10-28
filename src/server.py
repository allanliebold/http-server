# -*- coding: utf-8 -*-
"""Create a server socket to recieve a message from a client.

And send back a response.
"""

from __future__ import unicode_literals
import sys
import os
import socket


def server():
    """Build a server to rece/ive from client and respond."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 6667)
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
                resolve_uri(parse_request(req))
                conn.sendall(response_ok())
            except ValueError as message:
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
    """."""
    response_content = [type, content]
    uri_list = uri_string.split('/')
    if uri_list[-1] and '.' in uri_list[-1]:
        file_type = uri_string[-1].split('.')[1]
        if file_type == 'txt':
            file_type == 'text/plain'
        elif file_type == 'jpeg':
            file_type == 'image/jpeg'
        elif file_type == 'png':
            file_type == 'image/png'
        elif file_type == 'html':
            file_type == 'text/html'
        else:
            raise TypeError("File type not supported")
    else:
        ### uri is a directory - print as list

    return response_content


def response_ok():
    """Return a well formed HTTP 200 response."""
    #### take the resolved uri data and type and build a respponse to send.
    return b"HTTP/1.1 200\nOK\r\n"
### {}\r\nContent-Type: {}\r\n{}\r\n.format(resp_type, cont_type, cont_body).encode("utf-8")


def response_error(status, reason):
    """Return a well formed error for the status passed."""
    return "HTTP/1.1 {} {}".format(status, reason).encode('utf-8')

if __name__ == "__main__":
    """Run server."""
    server()
