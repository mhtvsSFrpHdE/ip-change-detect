from json import JSONDecodeError
import socket
import time
import os    # nopep8
import sys    # nopep8
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
from response import Response    # nopep8
import config    # nopep8
import custom_exception    # nopep8
import dns_resolver    # nopep8
import internet_alive    # nopep8

knownServerVersion = Response().serverVersion
knownServerIdentity = None
# Allow to update server identity if preshared key is match
knownPresharedKey = Response().presharedKey
serverInformationRecorded = False
retryCountOnDisconnect = 0
internetOnline = False


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

def getObjectTypeName(e):
    typeName = e.__class__.__name__
    return typeName

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            if internetOnline == False:
                internet_alive.testInternet()
                internetOnline = True

            serverAddress = dns_resolver.getCurrentDnsRecord(config.dnsResolver, config.dnsRecord)
            serverPort = config.serverPort
            print(f'Exist DNS record: {serverAddress}')

            # Connect
            s.connect((serverAddress, serverPort))
            resetRetryCountOnDisconnect()
            print(f'Connected to server {serverAddress}, {serverPort}')

            # Parse response
            data = s.recv(config.socketBufferLength)
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
            data = s.recv(config.socketBufferLength)
        except JSONDecodeError as e:
            # Failed to parse JSON, IP address may be changed
            # TODO: Update DDNS here

            exceptionTypeName = getObjectTypeName(e)
            print(f'{exceptionTypeName}: {e}')

            retry()
        except custom_exception.ServerInformationMismatchException as e:
            # Failed to verify preshared key, IP address may be changed
            # TODO: Update DDNS here

            exceptionTypeName = getObjectTypeName(e)
            print(f'{exceptionTypeName}: {e}')

            retry()
        except ConnectionResetError as e:
            # Long connection disconnected, IP address may be changed
            # TODO: Update DDNS here

            exceptionTypeName = getObjectTypeName(e)
            print(f'{exceptionTypeName}: {e}')

            retry()
        except ConnectionRefusedError as e:
            # Failed to connect server, address may be online but refused, IP address may be changed
            # TODO: Update DDNS here

            exceptionTypeName = getObjectTypeName(e)
            print(f'{exceptionTypeName}: {e}')

            retry()
        except TimeoutError as e:
            # Failed to connect server, timeout, address may be not exist, IP address may be changed
            # TODO: Update DDNS here

            exceptionTypeName = getObjectTypeName(e)
            print(f'{exceptionTypeName}: {e}')
        except dns_resolver.NoNameservers as e:
            # Failed to query exist ip address, DNS server may be offline

            exceptionTypeName = getObjectTypeName(e)
            print(f'{exceptionTypeName}: {e}')

            time.sleep(config.clientReconnectInterval)
            internetOnline = False
        except custom_exception.InternetOfflineException as e:
            # Failed to test internet, internet may be offline
            # The reason to use different exception from NoNameservers
            # You can know is internet alive server has no response
            # or DNS server has no response

            exceptionTypeName = getObjectTypeName(e)
            print(f'{exceptionTypeName}: {e}')

            time.sleep(config.clientReconnectInterval)
        except Exception as e:
            # Unknown is bad, stop future action

            exceptionTypeName = getObjectTypeName(e)
            print(f'UnknownException {exceptionTypeName}: {e}')

            break
