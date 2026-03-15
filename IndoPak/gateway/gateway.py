import socket
import threading

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 9000

def handle_client(client_socket):
    data = b""
    while b"\r\n\r\n" not in data:
        data += client_socket.recv(1)

    headers, rest = data.split(b"\r\n\r\n", 1)
    headers_text = headers.decode(errors="ignore")

    # Block admin paths
    if "/admin" in headers_text:
        client_socket.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\nBlocked")
        client_socket.close()
        return

    content_length = 0
    for line in headers_text.split("\r\n"):
        if line.lower().startswith("content-length"):
            content_length = int(line.split(":")[1].strip())

    body = rest
    while len(body) < content_length:
        body += client_socket.recv(1024)

    forwarded_request = headers + b"\r\n\r\n" + body

    backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend.connect((BACKEND_HOST, BACKEND_PORT))
    backend.sendall(forwarded_request)

    response = b""
    backend.settimeout(1)
    try:
        while True:
            chunk = backend.recv(4096)
            if not chunk:
                break
            response += chunk
    except:
        pass

    client_socket.sendall(response)
    backend.close()
    client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen(5)
    print("[+] Gateway listening on port 8080")

    while True:
        client, _ = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    main()
