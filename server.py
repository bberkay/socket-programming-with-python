"""
    Server
    ------

    - All descriptions and comments created by ChatGPT and GitHub Copilot
"""

import socket
import threading
import keyboard

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
        threading.Thread(target=self.__accept_connections).start()

        # Get the command from the server owner
        threading.Thread(target=self.__run_command).start()

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
                print(f"[Server] An error occurred while client({client_id}) handling, Error: {e}")

    def __run_command(self) -> None:
        """
            Run the command from the server owner.
        """

        # If the server owner presses the "q" key, stop the server
        keyboard.on_press_key("q", lambda _: self.stop())

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
        self.__broadcast(f"[Broadcast] {username} has joined the chat!", username)

        while True:
            try:
                # Get the message from the client
                message = client.recv(1024)

                # If the message is empty, the client has disconnected
                if not message:
                    # Close the client's connection
                    self.__close_client(client_id)
                    break
                else:
                    # Send the message to all clients
                    self.__broadcast(message, username)
            except:
                # If an error occurs, close the client's connection
                self.__close_client(client_id)
                break

    def __broadcast(self, message: str|bytes, sender_username: str | None = None) -> None:
        """
            Broadcast a message to all clients.
        """
        try:
            # Loop through all clients
            for client in self.__clients:
                # If the client is not the sender, send the message
                if self.__clients[client]["client_username"] != sender_username:
                    self.__clients[client]["client_socket"].send(message.encode("utf-8"))
        except:
            pass

    def __close_client(self, client_id: str) -> None:
        """
            Close a client's connection.
        """

        # Close the client's connection
        if client_id in self.__clients:
            self.__clients[client_id]["client_socket"].close()
            self.__broadcast(f"[Broadcast] {self.__clients[client_id]['client_username']} has left the chat!")
            print(f"[Server] {client_id} is closed.")
            del self.__clients[client_id]

    def stop(self) -> None:
        """
            Stop the server.
        """
        # Send a message to all clients that the server is closed
        self.__broadcast("[Broadcast] The server is closed!")

        # Close all client connections
        for client in self.__clients:
            self.__clients[client]["client_socket"].close()

        # Close the server
        self.__server.close()

        print("[Server] Server is closed.")

if __name__ == "__main__":
    server = Server()
    server.start()
