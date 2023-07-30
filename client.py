import socket
import threading
import keyboard

class Client:
    """
        Client class for the TCP client.
    """

    def __init__(self, host: str | None = None, port: int | None = None):
        """
            Constructor for the Client class.
        """

        # Set the host and port
        self.host = "127.0.0.1" if host is None else host
        self.port = 55555 if port is None else port
        self.__client = None

    def connect(self) -> None:
        """
            Connect to the server.
        """
        # Create a new socket
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.host, self.port))

        username = input("[Client] Enter your username: ")
        self.__client.send(username.encode("utf-8"))

        # Start receiving messages
        threading.Thread(target=self.__receive_messages).start()

        # Start sending messages
        threading.Thread(target=self.__run_command).start()

    def __receive_messages(self) -> None:
        """
            Receive messages from the server.
        """
        while True:
            try:
                message = self.__client.recv(1024).decode("utf-8")
                print(message)
            except:
                # If an error occurs while receiving messages, assume the connection is closed
                print("[Client] Disconnected from the server!")
                break

        self.disconnect()

    def __run_command(self) -> None:
        """
            Run the command from the server owner.
        """

        # If the user presses the "q" key, stop the client
        keyboard.on_press_key("q", lambda _: self.disconnect())

    def disconnect(self) -> None:
        """
            Disconnect from the server.
        """
        # Close the client socket
        self.__client.close()


if __name__ == "__main__":
    client = Client()
    client.connect()
