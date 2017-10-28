# HTTP Server

The server opens a socket and listens for requests sent by the client. If the request is successfully received and contains a 
well-formed HTTP request, the server will return an HTTP response with a status of 200 OK.

The server only accepts HTTP/1.1 GET requests that include a Host header. If these are not included and in the correct format a Python ValueError will be raised and an error response with the corresponding status code and reason will be sent back to the client.

Close the server with the keyboard command Ctrl-C. 

Authors:
Robert Bronson
Allan Liebold
