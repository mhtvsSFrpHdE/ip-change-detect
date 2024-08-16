import socket    # nopep8
import time    # nopep8
import os    # nopep8
import sys    # nopep8
import keepalive    # nopep8
import logging    # nopep8
from json import JSONDecodeError    # nopep8

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
import config    # nopep8
import example    # nopep8
import custom_exception    # nopep8
import log    # nopep8

import dns_resolver    # nopep8
import internet_alive    # nopep8
import ddns    # nopep8
import connect    # nopep8
import verify_server    # nopep8

log.initLog(config.logTypeClient)

while True:
    # Check internet
    if internet_alive.internetOnline == False:
        try:
            internet_alive.testInternet()
            internet_alive.internetOnline = True
            continue
        except custom_exception.InternetOfflineException as e:
            # Failed to test internet, internet may be offline
            # The reason to use different exception from NoNameservers
            # You can know is internet alive server has no response
            # or DNS server has no response

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            time.sleep(config.clientReconnectInterval)
            continue
    # Update DDNS if needed
    if connect.ddnsRequest == True:
        try:
            ddns.ddnsMain()
            connect.ddnsRequest = False
        except custom_exception.OpenDnsUnavailableException as e:
            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')
            log.printToLog("Open DNS unavailable, retrying")

            connect.ddnsRequest = True
        except custom_exception.CloudFlareException as e:
            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')
            log.printToLog("DDNS request failed, retrying")

            connect.ddnsRequest = True
        except custom_exception.InternetOfflineException as e:
            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')
            log.printToLog("DDNS request failed, internet offline, retrying")

            connect.ddnsRequest = True
            internet_alive.internetOnline = False
        continue

    # Connect to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            serverAddress = dns_resolver.getCurrentDnsRecord()
            serverPort = config.serverPort
            log.printToLog(f'Get server address from DNS record: {serverAddress}')

            # Connect
            s.settimeout(float(config.clientSocketTimeout))
            keepalive.set(s, after_idle_sec=config.keepaliveAfterIdleSec, interval_sec=config.keepaliveIntervalSec, max_fails=config.keepaliveMaxFails)
            s.connect((serverAddress, serverPort))
            connect.resetNetworkRetryCountOnDisconnect()
            log.printToLog(f'Connected to server {serverAddress}, port {serverPort}')

            # Parse response
            data = s.recv(config.socketBufferLength)
            responseAsJsonString = data.decode()
            response = verify_server.Response.fromJson(responseAsJsonString)
            connect.resetJsonDecodeErrorCountOnDisconnect()
            connect.resetServerTimeoutCountOnDisconnect()

            # Print response
            log.printToLog(f'name: {response.serverName}')
            log.printToLog(f'version: {response.serverVersion}')
            log.printToLog(f'identity: {response.serverIdentity}')
            log.printToLog(f'preshared key: {response.presharedKey}')

            # Debug code to test during server shutdown
            # s.close()

            if verify_server.serverInformationRecorded == False:
                verify_server.knownServerIdentity = response.serverIdentity
                verify_server.serverInformationRecorded = True

            # Compare server information
            sameVersion = verify_server.knownServerVersion == response.serverVersion
            samePresharedKey = verify_server.knownPresharedKey == response.presharedKey
            sameIdentity = verify_server.knownServerIdentity == response.serverIdentity
            sameServer = samePresharedKey

            if sameServer == False:
                verify_server.serverInformationRecorded = False
                # Disconnect
                raise custom_exception.ServerInformationMismatchException(f'Connected server information mismatch with known')
            else:
                log.printToLog('Server verified by preshared key')

            if sameVersion == False:
                log.printToLog('Server version is different than previous connected server', level=logging.WARNING)
            if sameIdentity == False:
                log.printToLog('Server identity is different than previous connected server', level=logging.WARNING)
                verify_server.knownServerIdentity = response.serverIdentity

            # Server will not send future response
            # Block at here, keep long connection
            s.settimeout(None)
            data = s.recv(config.socketBufferLength)
        except custom_exception.ClientDnsUnavailableException as e:
            # Can't get server address from DNS record, client dns has not response
            # This error has no solution to handle it, client dns must be success to continue

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            time.sleep(config.clientReconnectInterval)
        except JSONDecodeError as e:
            # Failed to parse JSON, connected to unknown server, IP address may be changed

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            connect.queueJsonDecodeError()
        except custom_exception.ServerInformationMismatchException as e:
            # Failed to verify preshared key, IP address may be changed

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            connect.queueNetworkRetry()
        except ConnectionResetError as e:
            # Long connection disconnected, IP address may be changed

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            connect.queueNetworkRetry()
        except ConnectionRefusedError as e:
            # Failed to connect server, address may be online but refused, IP address may be changed

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            connect.queueNetworkRetry()
        except TimeoutError as e:
            # Failed to connect server, timeout, address may be not exist,
            # connected to wrong server that not answer in certain time, IP address may be changed

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            connect.queueServerTimeout()
        except ConnectionAbortedError as e:
            # Connection disconnected, IP address may be changed

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            connect.queueNetworkRetry()
        except dns_resolver.NoNameservers as e:
            # Failed to query ip address, DNS server or internet may be offline

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            time.sleep(config.clientReconnectInterval)
            internet_alive.internetOnline = False
        except dns_resolver.LifetimeTimeout as e:
            # Failed to query ip address, DNS server or internet may be offline

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'{exceptionTypeName}: {e}')

            time.sleep(config.clientReconnectInterval)
            internet_alive.internetOnline = False
        except custom_exception.ExceptionPlaceholder as e:
            # Unknown is bad, stop future action

            exceptionTypeName = example.getObjectTypeName(e)
            log.printToLog(f'UnknownException {exceptionTypeName}: {e}')

            break
