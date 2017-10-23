import sys
import socket

def server():
    server = socket.socket(socket.AF_INET, 
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 6666)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()
    print(conn.recv(8).decode('utf8'))
    buffer_length = 8
    message_complete = False
    whole_msg = ''
    while not message_complete:
        part = conn.recv(buffer_length)
        whole_msg += part.decode('utf8')
        if len(part) < buffer_length:
            break
    print (whole_msg)

    response = "Darn that stupid lazy dog!"
    conn.sendall(response.encode('utf8'))