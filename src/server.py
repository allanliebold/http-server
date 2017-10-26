# -*- coding: utf-8 -*-
"""Create a server socket to recieve a message from a client.

And send back a response.
"""

import sys
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
            conn.sendall(response_ok())
            # conn.sendall(whole_msg.encode('utf-8'))
            conn.close()
    except KeyboardInterrupt:
            conn.close()
            server.close()
            print('Server closed')
            sys.exit()


def parse_response(request):
    """Parse Response function.

    If passed a well-formed HTTP/1.1 GET request, return the request URI.
    Otherwise, raise the appropriate exception.
    """
    if request[:3] != 'GET':
        return response_error('405')

    if request['HTTP'] != 'HTTP/1.1':
        return response_error('505')

    """If no errors arise, return the request URI."""
    return request['URI']


def response_ok():
    """Return a well formed HTTP 200 response."""
    return b"HTTP/1.1 200\nOK\r\n"


def response_error(status):
    """Return a well formed error for the status passed."""
    if status == '405':
        msg = b"HTTP/1.1 405\nMethod Not Allowed\r\n"

    if status == '500':
        msg = b"HTTP/1.1 500\nInternal Server Error\r\n"

    if status == '505':
        msg = b"HTTP/1.1 505\nHTTP Version Not Supported\r\n"

    return msg

if __name__ == "__main__":
    """Run server."""
    server()
