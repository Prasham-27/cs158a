#!/usr/bin/env python3
import socket
import ssl

def main():
    host = "www.google.com"
    port = 443
    output_file = "response.html"

    # Create a default SSL context with certificate validation
    context = ssl.create_default_context()

    # Create a TCP/IP socket
    with socket.create_connection((host, port)) as sock:
        # Wrap the socket with SSL
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            # Build a well-formed HTTP/1.1 GET request
            request_lines = [
                f"GET / HTTP/1.1",
                f"Host: {host}",
                "User-Agent: secureget/1.0",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language: en-US,en;q=0.5",
                "Connection: close",
                "",  # blank line to end headers
                ""
            ]
            request_data = "\r\n".join(request_lines).encode("utf-8")

            # Send the request
            ssock.sendall(request_data)

            # Receive the full response until the server closes the connection
            chunks = []
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
                chunks.append(data)

    # Combine received chunks
    raw_response = b"".join(chunks)

    # Separate headers and body by the first \r\n\r\n
    header_end = raw_response.find(b"\r\n\r\n")
    if header_end == -1:
        # Fallback: if no header/body split found, write everything
        body = raw_response
        headers = b""
    else:
        headers = raw_response[:header_end]
        body = raw_response[header_end + 4:]

    # print status line and some headers to console
    try:
        first_line = headers.split(b"\r\n", 1)[0].decode("iso-8859-1", errors="replace")
        print(f"Status: {first_line}")
    except Exception:
        pass

    # Save the body to response.html
    # Google may return compressed (gzip/br) or HTML depending on negotiation.
    # We didn't advertise compression explicitly, so likely plain HTML is returned.
    with open(output_file, "wb") as f:
        f.write(body)

    print(f"Wrote {len(body)} bytes to {output_file}")

if __name__ == "__main__":
    main()

