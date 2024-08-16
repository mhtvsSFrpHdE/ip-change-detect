class MaximumRetryCountException(Exception):
    pass

# In case of connected to wrong server, it may not response in certain time

class MaximumTimeoutCountException(Exception):
    pass

# In case of connected to wrong server, response may wrong

class MaximumJsonDecodeErrorCountException(Exception):
    pass

# In case of same preshared key, server may be rebooted


class ServerInformationMismatchException(Exception):
    pass

# In case of third party exception, store it in a variable
class RawException(Exception):
    rawException = None

class InternetOfflineException(RawException):
    pass

class CloudFlareException(RawException):
    pass

class OpenDnsUnavailableException(RawException):
    pass

class ClientDnsUnavailableException(RawException):
    pass

# Stop catch unknown exception, use this one for a while to actually catch nothing
class ExceptionPlaceholder(Exception):
    pass

# Must stop code execution on some case, raise this
class UnknownException(RawException):
    pass
