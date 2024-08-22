class MaximumRetryCountException(Exception):
    pass

class MaximumTimeoutCountException(Exception):
    pass

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

# Cloudflare API error
class DdnsProviderException(RawException):
    pass

# DNS resolver error
class DnsResolverException(RawException):
    pass

# If client keeps sending ddns request but the value is already online
# External address detection method may not reliable
class RedundantDdnsAttemptsException(RawException):
    pass

# Stop catch unknown exception, use this one for a while to actually catch nothing
class ExceptionPlaceholder(Exception):
    pass

# Must stop code execution on some case, raise this
class UnknownException(RawException):
    pass
