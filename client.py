import socket
import threading

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except:
            # If an error occurs while receiving messages, assume the connection is closed
            print("[Client] Connection to the server is closed.")
            break

def main():
    host = "127.0.0.1"
    port = 55555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input("[Client] Enter your username: ")
    client_socket.send(username.encode("utf-8"))

    # Start a new thread to receive messages from the server
    threading.Thread(target=receive_message, args=(client_socket,)).start()

    # Start sending messages to the server
    while True:
        message = input("[Client] Enter your message: ")
        client_socket.send(message.encode("utf-8"))

        if not message or message.lower() == "exit":
            # If the client wants to exit, close the connection
            break

    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    main()
