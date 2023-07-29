"""
    Server
    ------
    This class represents a simple TCP chat server that allows multiple clients to connect and
    communicate with each other in a chat-like environment.

    - All descriptions and comments created by ChatGPT and GitHub Copilot
"""

import socket
import threading


class Server:
    """
        Server class for the TCP server.
    """

    def __init__(self, host: str | None = None, port: int | None = None, max_connections: int | None = 5):
        """
            Constructor for the Server class.
        """

        # Set the host, port, and max connections
        self.host = "127.0.0.1" if host is None else host
        self.port = 55555 if port is None else port
        self.max_connections = max_connections
        self.__server = None
        self.__clients = {}

    def start(self) -> None:
        """
            Start the server.
        """
        # Create a new socket
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((self.host, self.port))
        self.__server.listen(self.max_connections)

        print(f"[Server] Server started on {self.host}:{self.port}")

        # Start accepting connections
        self.__accept_connections()

    def __accept_connections(self) -> None:
        """
            Accept connections from clients.
        """

        while True:
            client, address = self.__server.accept()
            client_id = f"{address[0]}:{address[1]}"
            print(f"[Server] {client_id} has connected!")

            try:
                # Start a new thread for the client
                threading.Thread(target=self.__handle_client, args=(client, client_id,)).start()
            except Exception as e:
                # If an error occurs, close the client's connection
                self.__close_client(client_id)
                self.__broadcast(f"[Broadcast] {self.__clients[client_id]['username']} unexpectedly disconnected!".encode("utf-8"))
                print(f"[Server] {client_id} has disconnected!")

    def __handle_client(self, client: socket.socket, client_id: str) -> None:
        """
            Handle a client.
        """
        # Get the client's username
        username = client.recv(1024).decode("utf-8")

        # Add the client to the list of clients
        self.__clients[client_id] = {"client_socket": client, "client_username": username}

        # Send a welcome message to the client
        client.send(f"[Server] Hi {username}, Welcome to the chat!".encode("utf-8"))

        # Send a message to all clients that the client has joined
        self.__broadcast(f"[Broadcast] {username} has joined the chat!".encode("utf-8"), username)

        while True:
            try:
                # Get the message from the client
                message = client.recv(1024)

                # If the message is empty, the client has disconnected
                if not message or message.decode("utf-8") == "exit":
                    self.__broadcast(f"[Broadcast] {username} has left the chat!".encode("utf-8"))
                    break

                # Send the message to all clients
                self.__broadcast(message, username)
            except Exception as e:
                # If an error occurs, close the client's connection
                self.__broadcast(f"[Broadcast] {username} unexpectedly disconnected!".encode("utf-8"), username)
                print(f"[Server] {client_id} has disconnected!")
                break

        # Close the client's connection
        self.__close_client(client_id)

    def __broadcast(self, message: bytes, username: str | None = None) -> None:
        """
            Broadcast a message to all clients.
        """
        try:
            # Loop through all clients
            for client in self.__clients:
                # If the client is not the sender, send the message
                if self.__clients[client]["client_username"] != username:
                    self.__clients[client]["client_socket"].send(f"[{username}] {message}")
        except Exception as e:
            print("[Server] An error occurred while broadcasting a message!")

    def __close_client(self, client_id: str) -> None:
        """
            Close a client's connection.
        """

        # Close the client's connection
        self.__clients[client_id]["client_socket"].close()
        del self.__clients[client_id]
        print(f"[Server] {client_id} is closed!")

    def stop(self) -> None:
        """
            Stop the server.
        """

        # Close the server's connection
        self.__server.close()


if __name__ == "__main__":
    server = Server()
    server.start()
