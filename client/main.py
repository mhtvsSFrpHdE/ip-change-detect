from json import JSONDecodeError
import socket
import time
import os    # nopep8
import sys    # nopep8
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
from response import Response    # nopep8
import config    # nopep8

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

knownServerName = None
knownServerVersion = Response().serverVersion
knownServerIdentity = None
knownPresharedKey = Response().presharedKey
serverInformationRecorded = False
retryCountOnDisconnect = 0


def retry():
    global retryCountOnDisconnect

    time.sleep(config.clientReconnectInterval)

    retryCountOnDisconnect = retryCountOnDisconnect + 1
    if retryCountOnDisconnect > config.clientRetryMaxCountOnDisconnect:
        raise Exception(f'Maximum retry count reached')


def resetRetryCountOnDisconnect():
    global retryCountOnDisconnect

    retryCountOnDisconnect = 0


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Connect
            s.connect((HOST, PORT))
            resetRetryCountOnDisconnect()
            print(f'Connected to server {HOST}, {PORT}')

            # Parse response
            data = s.recv(1024)
            responseAsJsonString = data.decode()
            response = Response.fromJson(responseAsJsonString)

            # Print response
            print(f'name: {response.serverName}')
            print(f'version: {response.serverVersion}')
            print(f'identity: {response.serverIdentity}')
            print(f'preshared key: {response.presharedKey}')

            # Remember server information, some property is fixed from config
            if serverInformationRecorded == False:
                knownServerName = response.serverName
                knownServerIdentity = response.serverIdentity
                serverInformationRecorded = True

            # Compare server information
            sameServerName = knownServerName == response.serverName
            sameServerVersion = knownServerVersion == response.serverVersion
            sameServerIdentity = knownServerIdentity == response.serverIdentity
            samePresharedKey = knownPresharedKey == response.presharedKey
            sameServer = sameServerName and sameServerVersion and sameServerIdentity and samePresharedKey
            if sameServer == False:
                serverInformationRecorded = False
                # Disconnect
                raise Exception(f'Connected server information mismatch')
            else:
                print('Server identity verified')

            # Server will not send future response
            # Block at here, keep long connection
            data = s.recv(1024)
        except JSONDecodeError as e:
            print(f'JSONDecodeError: {e}')
            try:
                retry()
            except Exception as e:
                print(f'RetryError: {e}')
                resetRetryCountOnDisconnect()
        except Exception as e:
            print(f'UnknownError: {e}')
            try:
                retry()
            except Exception as e:
                print(f'RetryError: {e}')
                resetRetryCountOnDisconnect()
