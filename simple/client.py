"""
    Client
    ------
    A simple TCP client that sends a message to the server and receives a response. The client will
    continue to send messages to the server until the user enters 'q' to quit. When the user quits,
    the client sends a message to the server to close the connection.

    - All descriptions and comments created by ChatGPT and GitHub Copilot

"""

import socket

# Server IP address and port number
server_ip = "127.0.0.1"  # localhost
server_port = 12345

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

while True:
    # Get the message from the user
    message = input("Enter your message (Press 'q' to quit): ")
    if message.lower() == "q":
        client_socket.send("Connection closed".encode())
        break

    # Send the message to the server
    client_socket.send(message.encode())

    # Receive the response from the server
    response = client_socket.recv(1024).decode()
    print("Response from the server:", response)

# Close the connection
client_socket.close()

"""
    Output:
    -------
    Enter your message (Press 'q' to quit): Hello
    Response from the server: Message received: Hello
    Enter your message (Press 'q' to quit): How are you?
    Response from the server: Message received: How are you?
    Enter your message (Press 'q' to quit): q
    Response from the server: Connection closed
"""