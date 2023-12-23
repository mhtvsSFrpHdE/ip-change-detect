# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        print("Ready for connection")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                try:
                    conn.sendall(b"IP change detector version 0.0.1")
                    data = conn.recv(1024)
                    if not data:
                        print(f"{addr} disconnected")
                        break
                except Exception as e:
                    print(e)
                    break
