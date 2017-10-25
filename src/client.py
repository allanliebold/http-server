# -*- coding: utf-8 -*-
"""Create a client socket to interact with a server socket."""


import sys
import socket


def client(message):
    """Instantiate a client socket that sends a message."""
    infos = socket.getaddrinfo('127.0.0.1', 6665)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    message += u'\xb8'
    if hasattr('', 'encode'):
        client.sendall(message.encode('utf8'))
    else:
        client.sendall(message)
    buffer_length = 8
    reply_complete = False
    whole_resp = ''
    while not reply_complete:
        part = client.recv(buffer_length)
        whole_resp += part.decode('utf8')
        if len(part) < buffer_length:
            break
    print(whole_resp)
    return whole_resp

if __name__ == "__main__":
    """Run client function passing sys.argv as a mesage."""
    client(sys.argv[1])