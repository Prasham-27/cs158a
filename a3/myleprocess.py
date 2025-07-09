# myleprocess.py

import socket
import threading
import uuid
import json
import time
import sys
import logging

class Message:
    def __init__(self, sender_uuid, flag):
        # Keep UUID as UUID object, not string
        if isinstance(sender_uuid, str):
            self.uuid = uuid.UUID(sender_uuid)
        else:
            self.uuid = sender_uuid
        self.flag = flag

    def to_json(self):
        """Serializes the message object to a JSON string, ending with a newline."""
        # Convert UUID to string for JSON serialization
        return json.dumps({"uuid": str(self.uuid), "flag": self.flag}) + "\n"

    @staticmethod
    def from_json(json_str):
        """Deserializes a JSON string back into a Message object."""
        data = json.loads(json_str)
        return Message(data['uuid'], data['flag'])

# Global state variables for the process
MY_UUID = uuid.uuid4()
LEADER_ID = None
IS_CANDIDATE = True
ELECTION_OVER = False

# Sockets and synchronization
client_socket = None
client_ready = threading.Event()

def setup_logging(log_file):
    """Configures logging to file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def send_message(msg):
    """A helper function to safely send a message after ensuring the client socket is ready."""
    global client_socket, client_ready
    client_ready.wait() 
    if client_socket:
        try:
            client_socket.sendall(msg.to_json().encode('utf-8'))
            logging.info(f"Sent: uuid={msg.uuid}, flag={msg.flag}")
        except OSError as e:
            logging.error(f"Failed to send message: {e}")
    else:
        logging.error("Cannot send message, client socket is not available.")

def process_message(msg_str):
    """The core logic for handling a received message."""
    global LEADER_ID, IS_CANDIDATE, ELECTION_OVER

    try:
        msg = Message.from_json(msg_str)
        
        # Now both are UUID objects, comparison will work
        comparison = "same"
        if msg.uuid > MY_UUID:
            comparison = "greater"
        elif msg.uuid < MY_UUID:
            comparison = "less"

        state_str = "1" if ELECTION_OVER else "0"
        logging.info(f"Received: uuid={msg.uuid}, flag={msg.flag}, {comparison}, {state_str}")
        
        if ELECTION_OVER:
            if LEADER_ID:
                logging.info(f"Leader ID: {LEADER_ID}")
            logging.info("Ignoring message, election is over.")
            return

        # Leader announcement message (flag=1)
        if msg.flag == 1:
            LEADER_ID = msg.uuid
            ELECTION_OVER = True
            logging.info(f"Leader is decided to {LEADER_ID}")
            # Forward the leader announcement if this node is not the leader
            if LEADER_ID != MY_UUID:
                send_message(msg)
            return

        # Regular election message (flag=0)
        if msg.uuid > MY_UUID:
            IS_CANDIDATE = False
            send_message(msg)
        elif msg.uuid < MY_UUID:
            logging.info("Ignoring message, received UUID is smaller.")
        else: # Received my own UUID back
            if IS_CANDIDATE:
                LEADER_ID = MY_UUID
                ELECTION_OVER = True
                logging.info(f"Leader is decided to {LEADER_ID}")
                leader_msg = Message(MY_UUID, 1)
                send_message(leader_msg)

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logging.error(f"Failed to process message: '{msg_str.strip()}', error: {e}")

def server_thread_func(host, port):
    """Thread function to run the server, listening for incoming messages."""
    global ELECTION_OVER
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    logging.info(f"Server listening on {host}:{port}")

    try:
        conn, addr = server_socket.accept()
        logging.info(f"Accepted connection from {addr}")
        
        buffer = ""
        with conn:
            while not ELECTION_OVER:
                try:
                    data = conn.recv(1024)
                    if not data:
                        logging.warning("Connection closed by peer. Stopping server thread.")
                        break
                    
                    buffer += data.decode('utf-8')
                    while '\n' in buffer:
                        message, buffer = buffer.split('\n', 1)
                        if message.strip():
                           process_message(message.strip())
                except ConnectionResetError:
                    logging.warning("Connection reset by peer.")
                    break
                except Exception as e:
                    logging.error(f"Error in server loop: {e}")
                    break
    except Exception as e:
        logging.error(f"Server thread crashed: {e}")
    finally:
        ELECTION_OVER = True
        logging.info("Server thread finished.")
        server_socket.close()

def main():
    """Main function to initialize and run the process."""
    global client_socket, client_ready, ELECTION_OVER

    if len(sys.argv) != 3:
        print("Usage: python myleprocess.py <config_file> <log_file>")
        sys.exit(1)

    config_file, log_file = sys.argv[1], sys.argv[2]
    
    setup_logging(log_file)
    logging.info(f"My Process UUID is {MY_UUID}")

    with open(config_file, 'r') as f:
        server_line = f.readline().strip().split(',')
        client_line = f.readline().strip().split(',')

    server_host, server_port = server_line[0], int(server_line[1])
    client_host, client_port = client_line[0], int(client_line[1])

    s_thread = threading.Thread(target=server_thread_func, args=(server_host, server_port))
    s_thread.start()

    time.sleep(2) 

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((client_host, client_port))
        logging.info(f"Connected to client at {client_host}:{client_port}")
        client_ready.set()
    except Exception as e:
        logging.error(f"Client connection failed: {e}")
        ELECTION_OVER = True
        client_ready.set()
        return
    
    if not ELECTION_OVER:
        initial_msg = Message(MY_UUID, 0)
        send_message(initial_msg)

    # Wait for the election to complete
    while not ELECTION_OVER:
        if not s_thread.is_alive():
            logging.error("Server thread died unexpectedly. Exiting.")
            break
        time.sleep(0.1)

    # Give time for final messages
    time.sleep(2)

    if client_socket:
        client_socket.close()
    
    s_thread.join(timeout=2)
    logging.info("Process finished.")
    if LEADER_ID:
        print(f"Leader is {LEADER_ID}")

if __name__ == "__main__":
    main()

