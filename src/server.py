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
            try:
                parse_request(whole_msg[:-3])
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


def response_ok():
    """Return a well formed HTTP 200 response."""
    return b"HTTP/1.1 200\nOK\r\n"


def response_error(status, reason):
    """Return a well formed error for the status passed."""
    return b"HTTP/1.1 {} \n {} \r\n".format(status, reason)

if __name__ == "__main__":
    """Run server."""
    server()
