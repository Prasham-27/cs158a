import socket

HOST = ''  # Listen on all interfaces
PORT = 12345
BUFSIZE = 64

def recv_all(conn, length):
    data = b''
    while len(data) < length:
        chunk = conn.recv(min(BUFSIZE, length - len(data)))
        if not chunk:
            break
        data += chunk
    return data

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f"Server listening on port {PORT}")
        while True:
            conn, addr = server_sock.accept()
            with conn:
                print(f"Connected from {addr[0]}")
                # Read 2-byte length header
                header = recv_all(conn, 2)
                if not header or len(header) < 2:
                    print("Connection closed (no header)")
                    continue
                msg_len = int(header.decode())
                print(f"msg_len: {msg_len}")
                # Read message
                msg = recv_all(conn, msg_len).decode()
                print(f"processed: {msg}")
                # Respond with uppercase
                response = header + msg.upper().encode()
                conn.sendall(response)
                print(f"msg_len_sent: {msg_len}")
                print("Connection closed")

if __name__ == "__main__":
    main()

