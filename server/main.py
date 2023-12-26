import socket
import os    # nopep8
import sys    # nopep8
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
from response import Response    # nopep8

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Use preshared key as identity, emulate disconnect caused by network fluctuations
debugFixedIdentity = True

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
                    response = Response()
                    if debugFixedIdentity:
                        response.serverIdentity = response.presharedKey
                    responseAsJsonString = response.toJson()
                    conn.sendall(responseAsJsonString.encode())
                    data = conn.recv(1024)
                    if not data:
                        print(f"{addr} disconnected")
                        break
                except Exception as e:
                    print(e)
                    break
