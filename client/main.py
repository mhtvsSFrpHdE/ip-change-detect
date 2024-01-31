from json import JSONDecodeError
import socket
import time
import os    # nopep8
import sys    # nopep8
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
from response import Response    # nopep8
import config    # nopep8
import custom_exception

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

knownServerVersion = Response().serverVersion
knownServerIdentity = None
# Allow to update server identity if preshared key is match
knownPresharedKey = Response().presharedKey
serverInformationRecorded = False
retryCountOnDisconnect = 0


def updateRetryCount():
    global retryCountOnDisconnect

    time.sleep(config.clientReconnectInterval)

    retryCountOnDisconnect = retryCountOnDisconnect + 1
    if retryCountOnDisconnect > config.clientRetryMaxCountOnDisconnect:
        raise custom_exception.MaximumRetryCountException(f'Maximum retry count reached')

def retry():
    try:
        updateRetryCount()
    except custom_exception.MaximumRetryCountException as e:
        print(f'RetryError: {e}')
        resetRetryCountOnDisconnect()

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

            if serverInformationRecorded == False:
                knownServerIdentity = response.serverIdentity
                serverInformationRecorded = True

            # Compare server information
            sameVersion = knownServerVersion == response.serverVersion
            samePresharedKey = knownPresharedKey == response.presharedKey
            sameIdentity = knownServerIdentity == response.serverIdentity
            sameServer = samePresharedKey

            if sameServer == False:
                serverInformationRecorded = False
                # Disconnect
                raise custom_exception.ServerInformationMismatchException(f'Connected server information mismatch with known')
            else:
                print('Server identity verified')

            if sameVersion == False:
                print('Warning: Server version is different')
            if sameIdentity == False:
                print('Warning: Server identity is different')
                knownServerIdentity = response.serverIdentity

            # Server will not send future response
            # Block at here, keep long connection
            data = s.recv(1024)
        except JSONDecodeError as e:
            print(f'JSONDecodeError: {e}')

            # Failed to parse JSON, IP address may be changed
            # TODO: Update DDNS here

            retry()
        except custom_exception.ServerInformationMismatchException as e:
            print(f'ServerInformationError: {e}')

            # Failed to verify preshared key, IP address may be changed
            # TODO: Update DDNS here

            retry()
        except ConnectionResetError as e:
            print(f'ConnectionResetError: {e}')

            # Long connection disconnected, IP address may be changed
            # TODO: Update DDNS here

            retry()
        except ConnectionRefusedError as e:
            print(f'ConnectionRefusedError: {e}')

            # Failed to connect server, IP address may be changed
            # TODO: Update DDNS here

            retry()
        except Exception as e:
            print(f'UnknownError: {e}')

            # Unknown is bad, stop future action
            break
