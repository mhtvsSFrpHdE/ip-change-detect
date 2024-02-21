import time    # nopep8

import config    # nopep8
import custom_exception    # nopep8
import example    # nopep8
import log    # nopep8

networkRetryCountOnDisconnect = 0
serverTimeoutCountOnDisconnect = 0
jsonDecodeErrorCountOnDisconnect = 0

ddnsRequest = False

def queueDdnsRequest():
    global ddnsRequest

    ddnsRequest = True
    log.printToLog('DDNS request queued')

def resetNetworkRetryCountOnDisconnect():
    global networkRetryCountOnDisconnect

    networkRetryCountOnDisconnect = 0

def resetServerTimeoutCountOnDisconnect():
    global serverTimeoutCountOnDisconnect

    serverTimeoutCountOnDisconnect = 0

def resetJsonDecodeErrorCountOnDisconnect():
    global jsonDecodeErrorCountOnDisconnect

    jsonDecodeErrorCountOnDisconnect = 0

def updateNetworkRetryCount():
    global networkRetryCountOnDisconnect

    time.sleep(config.clientReconnectInterval)

    networkRetryCountOnDisconnect = networkRetryCountOnDisconnect + 1
    if networkRetryCountOnDisconnect > config.clientRetryMaxCountOnDisconnect:
        raise custom_exception.MaximumRetryCountException(f'Maximum retry count reached')

def updateServerTimeoutCount():
    global serverTimeoutCountOnDisconnect

    time.sleep(config.clientReconnectInterval)

    serverTimeoutCountOnDisconnect = serverTimeoutCountOnDisconnect + 1
    if serverTimeoutCountOnDisconnect > config.clientTimeoutMaxCountOnDisconnect:
        raise custom_exception.MaximumTimeoutCountException(f'Maximum timeout count reached')

def updateJsonDecodeErrorCount():
    global jsonDecodeErrorCountOnDisconnect

    time.sleep(config.clientReconnectInterval)

    jsonDecodeErrorCountOnDisconnect = jsonDecodeErrorCountOnDisconnect + 1
    if jsonDecodeErrorCountOnDisconnect > config.clientJsonDecodeErrorMaxCountOnDisconnect:
        raise custom_exception.MaximumJsonDecodeErrorCountException(f'Maximum timeout count reached')

def queueNetworkRetry():
    try:
        # Retry without DDNS request
        updateNetworkRetryCount()
    except custom_exception.MaximumRetryCountException as e:
        # Retry count running out, queue DDNS request
        exceptionTypeName = example.getObjectTypeName(e)
        log.printToLog(f'{exceptionTypeName}: {e}')

        resetNetworkRetryCountOnDisconnect()
        queueDdnsRequest()

def queueServerTimeout():
    try:
        # Timeout without DDNS request
        updateServerTimeoutCount()
    except custom_exception.MaximumTimeoutCountException as e:
        # Timeout count running out, queue DDNS request
        exceptionTypeName = example.getObjectTypeName(e)
        log.printToLog(f'{exceptionTypeName}: {e}')

        resetServerTimeoutCountOnDisconnect()
        queueDdnsRequest()

def queueJsonDecodeError():
    try:
        # JSON decode error without DDNS request
        updateJsonDecodeErrorCount()
    except custom_exception.MaximumJsonDecodeErrorCountException as e:
        # JSON decode error count running out, queue DDNS request
        exceptionTypeName = example.getObjectTypeName(e)
        log.printToLog(f'{exceptionTypeName}: {e}')

        resetJsonDecodeErrorCountOnDisconnect()
        queueDdnsRequest()
