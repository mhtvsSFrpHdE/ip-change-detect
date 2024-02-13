import socket    # nopep8
import os    # nopep8
import sys    # nopep8
import keepalive    # nopep8
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
from response import Response    # nopep8
import config    # nopep8
import custom_exception    # nopep8

HOST = config.serverListenAddress
PORT = config.serverPort

# Use preshared key as identity, emulate disconnect caused by network fluctuations
debugFixedIdentity = True

response = Response()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    keepalive.set(s, after_idle_sec=1, interval_sec=1, max_fails=5)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        print("Ready for connection")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                try:
                    if debugFixedIdentity:
                        response.serverIdentity = response.presharedKey
                    responseAsJsonString = response.toJson()
                    conn.sendall(responseAsJsonString.encode())
                    data = conn.recv(config.socketBufferLength)
                    if not data:
                        print(f"{addr} disconnected")
                        break
                except custom_exception.ExceptionPlaceholder as e:
                    print(e)
                    break
