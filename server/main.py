import socket    # nopep8
import os    # nopep8
import sys    # nopep8
import selectors    # nopep8
import keepalive    # nopep8

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
from response import Response    # nopep8
import config    # nopep8
import example    # nopep8
import log    # nopep8

log.initLog(config.logTypeServer)

HOST = config.serverListenAddress
PORT = config.serverPort
response = Response()
selector = selectors.DefaultSelector()
connectionCount = 0

class ConnectionCallback():
    def __init__(self, callback, data):
        self.callback = callback
        self.data = data

# IO multiplexing recv
def recvCallback(data):
    global connectionCount

    conn, addr = data
    try:
        receive = conn.recv(config.socketBufferLength)
        if not receive:
            pass
    except ConnectionResetError as e:
        exceptionTypeName = example.getObjectTypeName(e)
        log.printToLog(f'{exceptionTypeName}: {e}')

    log.printToLog(f"Disconnected by {addr}")
    selector.unregister(conn)
    conn.close()
    connectionCount = connectionCount - 1

# IO multiplexing accept
def acceptCallback(serverSocket):
    global connectionCount

    conn, addr = serverSocket.accept()
    conn.setblocking(False)
    log.printToLog(f"Connected by {addr}")

    connectionCount = connectionCount + 1
    if connectionCount > config.serverMaxConnection:
        conn.close()
        connectionCount = connectionCount - 1
        log.printToLog(f"Connection limit {connectionCount} exceeded, connection closed")
        return

    selectorData = ConnectionCallback(recvCallback, (conn, addr))
    selector.register(conn, selectors.EVENT_READ, data=selectorData)

    if config.debugServerFixIdentity:
        response.serverIdentity = response.presharedKey
    responseAsJsonString = response.toJson()
    try:
        conn.sendall(responseAsJsonString.encode())
    except ConnectionResetError as e:
        exceptionTypeName = example.getObjectTypeName(e)
        log.printToLog(f'{exceptionTypeName}: {e}')

# Create and listen server socket
serverSocket = socket.socket()
keepalive.set(serverSocket, after_idle_sec=config.keepaliveAfterIdleSec, interval_sec=config.keepaliveIntervalSec, max_fails=config.keepaliveMaxFails)
serverSocket.bind((HOST, PORT))
serverSocket.listen()
serverSocket.setblocking(False)
selectorData = ConnectionCallback(acceptCallback, serverSocket)
selector.register(serverSocket, selectors.EVENT_READ, data=selectorData)

# Server event loop
while True:
    log.printToLog("Ready for connection")
    events = selector.select()
    for key, mask in events:
        selectorData = key.data
        selectorData.callback(selectorData.data)
