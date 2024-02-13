import config    # nopep8
import dns.resolver    # nopep8
import custom_exception    # nopep8

def testInternet():
    try:
        # Test internet
        # The idea is your environment should be at least allow 53 UDP available to use
        # ICMP ping needs admin permission if not using system ping.exe
        # so send a DNS query to the internet alive server, if get response, it is online
        dns.resolver.resolve_at(where=config.internetAliveServer, qname=config.internetAliveQuery, rdtype=config.dnsRecordType)

        # dns.resolver.reset_default_resolver() see README.md
        # From offline to online
        dns.resolver.reset_default_resolver()
    except Exception as e:
        raise custom_exception.InternetOfflineException("Internet offline")
