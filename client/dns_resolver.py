import dns.resolver    # nopep8
from dns.resolver import NoNameservers    # nopep8
from dns.resolver import LifetimeTimeout    # nopep8

import config    # nopep8
import internet_alive    # nopep8
import custom_exception    # nopep8

def getExternalIpAddress():
    try:
        # Specify IPv4 dns server address here, by default resolver1.opendns.com resolve to IPv6 OpenDNS server
        # And will return only IPv6 record, IPv4 record is dns.resolver.NoAnswer
        # where="resolver1.opendns.com" IPv4 record
        answer = dns.resolver.resolve_at(where="208.67.222.222", qname="myip.opendns.com", rdtype="A")
    except dns.resolver.LifetimeTimeout as e:
        try:
            internet_alive.testInternet()
        except custom_exception.InternetOfflineException as internetOfflineException:
            raise internetOfflineException

        openDnsUnavailableException = custom_exception.OpenDnsUnavailableException()
        openDnsUnavailableException.rawException = e
        raise openDnsUnavailableException

    externalIpAddress = answer[0].to_text()
    return externalIpAddress

def getCurrentDnsRecord():
    if config.clientIPv6Mode == False:
        if config.debugClientConnectToListenAddress == True:
            return config.serverListenAddress

        try:
            answer = dns.resolver.resolve_at(where=config.clientDnsResolver, qname=config.clientDnsRecord, rdtype="A")
        except dns.resolver.LifetimeTimeout as e:
            try:
                internet_alive.testInternet()
            except custom_exception.InternetOfflineException as internetOfflineException:
                raise internetOfflineException

            clientDnsUnavailableException = custom_exception.ClientDnsUnavailableException()
            clientDnsUnavailableException.rawException = e
            raise clientDnsUnavailableException

        currentIpAddress = answer[0].to_text()
        return currentIpAddress
    if config.clientIPv6Mode == True:
        try:
            answer = dns.resolver.resolve_at(where=config.clientDnsResolver, qname=config.clientDnsRecord6, rdtype="AAAA")
        except dns.resolver.LifetimeTimeout as e:
            try:
                internet_alive.testInternet()
            except custom_exception.InternetOfflineException as internetOfflineException:
                raise internetOfflineException

            clientDnsUnavailableException = custom_exception.ClientDnsUnavailableException()
            clientDnsUnavailableException.rawException = e
            raise clientDnsUnavailableException

        currentIpAddress = answer[0].to_text()
        return currentIpAddress
