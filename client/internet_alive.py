import config    # nopep8
import dns.resolver    # nopep8
import custom_exception    # nopep8

internetOnline = False

def testInternet():
    try:
        # Test internet
        # The idea is your environment should be at least allow 53 UDP available to use
        # ICMP ping needs admin permission if not using system ping.exe
        # so send a DNS query to the internet alive server, if get response, it is online
        dns.resolver.resolve_at(where=config.clientInternetAliveServer, qname=config.clientInternetAliveQuery, rdtype=config.clientDnsRecordType)

        # dns.resolver.reset_default_resolver() see README.md
        # From offline to online
        dns.resolver.reset_default_resolver()
    except dns.resolver.NoNameservers as e:
        internetOfflineException = custom_exception.InternetOfflineException("Internet offline")
        internetOfflineException.rawException = e
        raise internetOfflineException
    except dns.resolver.LifetimeTimeout as e:
        internetOfflineException = custom_exception.InternetOfflineException("Internet offline")
        internetOfflineException.rawException = e
        raise internetOfflineException
