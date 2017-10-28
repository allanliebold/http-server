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
            req = whole_msg[:-3]
            sys.stdout.write(req)
            conn.sendall(response_ok())
            # conn.sendall(whole_msg.encode('utf-8'))
            conn.close()
    except KeyboardInterrupt:
            conn.close()
            server.close()
            print('Server closed')
            sys.exit()


def response_ok():
    """Return a well formed HTTP 200 response."""
    return b"HTTP/1.1 200\nOK\r\n"


def response_error():
    """Return a well formed HTTP 500 server error."""
    return b"HTTP/1.1 500\nInternal Server Error\r\n"


if __name__ == "__main__":
    """Run server."""
    server()
