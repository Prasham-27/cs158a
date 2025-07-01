# mychatserver.py

import socket
import threading

# --- Server Configuration ---
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
BUFSIZE = 1024      # Buffer size for receiving data

# --- Server State ---
clients = []  # List to keep track of connected client sockets
lock = threading.Lock() # Lock for thread-safe operations on the clients list

def broadcast(message, sender_conn):
    """
    Broadcasts a message to all clients in the chat room except the sender.
    The message is formatted with the sender's port number.
    """
    # Get the sender's port number to prepend to the message
    sender_port = sender_conn.getpeername()[1]
    formatted_message = f"{sender_port}: {message}".encode('utf-8')
    
    # Use a lock to safely iterate over the list of clients
    with lock:
        for client_conn in clients:
            # Send the message to all clients except the one who sent it
            if client_conn != sender_conn:
                try:
                    client_conn.send(formatted_message)
                except socket.error:
                    # If sending fails, assume the client is disconnected.
                    # The main handling loop for that client will perform cleanup.
                    pass

def handle_client(conn, addr):
    """
    This function is executed in a separate thread for each connected client.
    It handles receiving messages from a client and initiating broadcasts.
    """
    port = addr[1]
    print(f"New connection from ('{addr[0]}', {port})")
    
    # Add the new client to the global list of clients
    with lock:
        clients.append(conn)

    try:
        while True:
            # Receive data from the client (up to 1024 bytes)
            message = conn.recv(BUFSIZE).decode('utf-8')
            
            if not message:
                # An empty message indicates the client has disconnected
                break
            
            # If the client sends 'exit', terminate their connection
            if message.strip().lower() == 'exit':
                break
            
            # Print the message to the server's console
            print(f"{port}: {message.strip()}")
            
            # Broadcast the message to other clients
            broadcast(message.strip(), conn)

    except ConnectionResetError:
        # This error occurs if the client closes the connection abruptly
        print(f"Client {addr} disconnected unexpectedly.")
    finally:
        # This block ensures cleanup happens regardless of how the loop exits
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"Connection from ('{addr[0]}', {port}) closed.")

def start_server():
    """
    Initializes and starts the chat server.
    """
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This option allows the socket to be reused immediately after it's closed
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))
        # Start listening for incoming connections
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        # Main loop to accept new connections
        while True:
            # Wait for a new connection
            conn, addr = server_socket.accept()
            
            # Create a new thread for each client to handle them concurrently
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    finally:
        # Cleanly close all connections and the server socket
        with lock:
            for conn in clients:
                conn.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()

