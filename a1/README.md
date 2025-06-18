# CS158A Assignment 1: Variable-Length Message TCP Client/Server

## Overview

This assignment implements a TCP client and server in Python that can exchange variable-length messages.  
The message protocol uses a 2-byte ASCII header to specify the message length (between 1 and 99 characters), followed by the message text.  
Both client and server use a buffer size (`bufsize`) of 64 bytes for all `send` and `recv` operations.

- **Server:** Receives a message from the client, converts it to uppercase, and sends it back with the same 2-byte length header.
- **Client:** Sends a message to the server and prints the uppercase response.

---

---

## How to Run

1. **Start the server** in one terminal:

    ```
    python myvlserver.py
    ```

2. **Start the client** in another terminal:

    ```
    python myvlclient.py
    ```

---

## Example Execution

**Server Terminal Output:**
Server listening on port 12345
Connected from 127.0.0.1
msg_len: 10
processed: helloworld
msg_len_sent: 10
Connection closed


**Client Terminal Output:**
Input lowercase sentence (max 99 chars): helloworld
From Server: HELLOWORLD
