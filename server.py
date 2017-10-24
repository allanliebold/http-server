"""Create a server socket to recieve a message from a client.

And send back a response.
"""

import sys
import socket


def server():
    """Build a server to receive from client and respond."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 6666)
    server.bind(address)
    server.listen(1)
    listening = True
    while listening:
        try:
            conn, addr = server.accept()
            buffer_length = 8
            message_complete = False
            whole_msg = ''
            while not message_complete:
                part = conn.recv(buffer_length)
                whole_msg += part.decode('utf8')
                if len(part) < buffer_length:
                    break
            print(whole_msg)
            response = "Server received message"
            conn.sendall(response.encode('utf8'))
        except KeyboardInterrupt:
            conn.close()
            server.close()
            sys.exit()

if __name__ == "__main__":
    """Run server."""
    server()
