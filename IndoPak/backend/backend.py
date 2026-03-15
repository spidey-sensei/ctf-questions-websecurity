import socket

FLAG = "CultRang{5om3tim3s_5muggl1ng_i5_G00d}"

def parse_requests(data):
    requests = []

    while True:
        if b"\r\n\r\n" not in data:
            break

        header_block, data = data.split(b"\r\n\r\n", 1)
        headers_text = header_block.decode(errors="ignore")
        lines = headers_text.split("\r\n")
        request_line = lines[0]

        body = b""

        if any(h.lower().startswith("transfer-encoding: chunked") for h in lines):
            while True:
                size_line, data = data.split(b"\r\n", 1)
                size = int(size_line.strip(), 16)
                if size == 0:
                    data = data.split(b"\r\n", 1)[1]
                    break
                body += data[:size]
                data = data[size+2:]

        requests.append((request_line, headers_text))

    return requests


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 9000))
    server.listen(5)
    print("[+] Backend listening on port 9000")

    while True:
        client, _ = server.accept()
        data = client.recv(16384)

        requests = parse_requests(data)
        response = b""

        for request_line, headers in requests:
            if (
                request_line.startswith("GET /admin/flag")
                and "X-Internal-Access: true" in headers
            ):
                response += (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: text/plain\r\n\r\n"
                    + FLAG.encode()
                )
            else:
                response += (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: text/plain\r\n\r\nOK"
                )

        client.sendall(response)
        client.close()


if __name__ == "__main__":
    main()
