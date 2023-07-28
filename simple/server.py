"""
    Server
    ------
    This is a simple TCP server that listens for connections from clients. When a client connects,
    the server receives a message from the client, prints it, and sends a response message back to
    the client. The server then waits for the next message from the client. The server will continue
    to receive messages from the client until the client sends a message to close the connection.

    - All descriptions and comments created by ChatGPT and GitHub Copilot

"""

import socket

# IP address and port number the server will listen on
server_ip = "127.0.0.1"  # localhost
server_port = 12345

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the IP and port
server_socket.bind((server_ip, server_port))

# Set the maximum number of connections
server_socket.listen(1)
print("Server is listening...")

# Accept the connection
conn, addr = server_socket.accept()
print("Connection received from:", addr)

while True:
    # Receive data from the client
    data = conn.recv(1024).decode()
    if not data:
        break  # Break the loop if no data is received

    print("Data received from the client: ", data)

    # Send a response message back
    message = "Message received: " + data
    conn.send(message.encode())

# Close the connection
conn.close()

"""
    Output:
    -------
    Server is listening...
    Connection received from: ('127.0.0.1', 12345)
    Data received from the client:  Hello
    Data received from the client:  How are you?
    Data received from the client:  Connection closed
"""
