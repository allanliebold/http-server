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
    address = ('127.0.0.1', 6665)
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
                whole_msg += part.decode('utf8')
                if len(part) < buffer_length:
                    break
                elif part[-1:] == '\xb8':
                    break
            print(whole_msg[:-1])
            response = 'Server received message'
            conn.sendall(response.encode('utf8'))
            conn.close()
    except KeyboardInterrupt:
            conn.close()
            server.close()
            print('Server closed')
            sys.exit()

if __name__ == "__main__":
    """Run server."""
    server()