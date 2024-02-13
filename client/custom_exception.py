class MaximumRetryCountException(Exception):
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
