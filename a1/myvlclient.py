import socket

HOST = '127.0.0.1'
PORT = 12345
BUFSIZE = 64

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        chunk = sock.recv(min(BUFSIZE, length - len(data)))
        if not chunk:
            break
        data += chunk
    return data

def main():
    sentence = input("Input lowercase sentence (max 99 chars): ")
    msg_len = len(sentence)
    if not (1 <= msg_len <= 99):
        print("Message length must be between 1 and 99.")
        return
    header = f"{msg_len:02}".encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(header + sentence.encode())
        # Receive response
        header_resp = recv_all(sock, 2)
        if not header_resp or len(header_resp) < 2:
            print("No response from server.")
            return
        resp_len = int(header_resp.decode())
        resp_msg = recv_all(sock, resp_len).decode()
        print("From Server:", resp_msg)

if __name__ == "__main__":
    main()

