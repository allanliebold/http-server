import sys
import socket

def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 6666)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()
    print(conn.recv(8).decode('utf8'))
