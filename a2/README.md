# CS158a - Assignment 2: Multi-Client Chat Server

This project implements a multi-threaded TCP chat server and a corresponding client in Python. The server can handle multiple clients concurrently, broadcasting messages from any client to all other connected clients.

## How to Run

You will need at least two separate terminal windows: one for the server and at least one for a client.

### 1. Start the Server

In the first terminal, navigate to the `a2` directory and run the server script:
```
python3 mychatserver.py
```
The server will start and print a message indicating it's listening for connections.

`Server listening on 127.0.0.1:12345`

### 2. Start the Client(s)

In one or more new terminal windows, navigate to the `a2` directory and run the client script:
```
python3 mychatclient.py
```
Each client will connect to the server. You can now type messages and press Enter to send them. Messages from other clients will appear in your terminal. To leave the chat, simply type `exit` and press Enter.

## Execution Example

Here is an example of a chat session with one server and three clients.

### Server Terminal
```
Server listening on 127.0.0.1:12345
New connection from ('127.0.0.1', 51044)
New connection from ('127.0.0.1', 51045)
New connection from ('127.0.0.1', 51047)
51044: Hi!
51045: Hello!
51047: How are you guys doing?
51045: Good.
Connection from ('127.0.0.1', 51044) closed.
Connection from ('127.0.0.1', 51047) closed.
Connection from ('127.0.0.1', 51045) closed.
```
### Client 1 Terminal (Port 51044)
```
Connected to chat server. Type 'exit' to leave.
Hi!
51045: Hello!
51047: How are you guys doing?
51045: Good.
exit
Disconnected from server.
```
### Client 2 Terminal (Port 51045)
```
Connected to chat server. Type 'exit' to leave.
51044: Hi!
Hello!
51047: How are you guys doing?
Good.
exit
Disconnected from server.
```
### Client 3 Terminal (Port 51047)
```
Connected to chat server. Type 'exit' to leave.
51044: Hi!
51045: Hello!
How are you guys doing?
51045: Good.
exit
Disconnected from server.
```
