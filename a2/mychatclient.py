# mychatclient.py

import socket
import threading
import sys

# --- Client Configuration ---
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
BUFSIZE = 1024      # Buffer size for receiving data

def receive_messages(client_socket):
    """
    Target function for the receiving thread.
    Handles receiving messages from the server and printing them to the console.
    """
    while True:
        try:
            # Receive and decode message from the server
            message = client_socket.recv(BUFSIZE).decode('utf-8')
            if message:
                print(message)
            else:
                # If the server sends an empty string, it means the connection is closed
                print("Server has closed the connection. Exiting...")
                break
        except (OSError, ConnectionAbortedError):
            # This handles cases where the socket is closed by the main thread
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    
    # Close the socket when the loop is broken
    client_socket.close()


def start_client():
    """
    Initializes the client, connects to the server, and manages threads for sending and receiving.
    """
    # Create a TCP/IP socket for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Try to connect to the server
    try:
        client_socket.connect((HOST, PORT))
        print("Connected to chat server. Type 'exit' to leave.")
    except ConnectionRefusedError:
        print("Connection failed. Please ensure the server is running.")
        sys.exit(1)

    # Create and start a daemon thread for receiving messages
    # A daemon thread will exit automatically when the main program finishes
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    # The main thread handles sending user input to the server
    try:
        while True:
            # Wait for user input
            message_to_send = input()
            
            # Send the message to the server
            client_socket.send(message_to_send.encode('utf-8'))
            
            # If the user types 'exit', break the loop to close the client
            if message_to_send.strip().lower() == 'exit':
                break
    except (KeyboardInterrupt, EOFError):
        # Handle Ctrl+C or Ctrl+D to gracefully exit
        print("\nLeaving the chat.")
        client_socket.send('exit'.encode('utf-8'))
    finally:
        # Cleanly close the connection and terminate
        client_socket.close()
        print("Disconnected from server.")
        sys.exit(0)

if __name__ == "__main__":
    start_client()

