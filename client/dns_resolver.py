import dns.resolver    # nopep8
from dns.resolver import NoNameservers    # nopep8
from dns.resolver import LifetimeTimeout    # nopep8

import config    # nopep8

def getExternalIpAddress():
    answer = dns.resolver.resolve_at(where="resolver1.opendns.com", qname="myip.opendns.com", rdtype=config.clientDnsRecordType)
    externalIpAddress = answer[0].to_text()
    return externalIpAddress

def getCurrentDnsRecord():
    if config.debugClientConnectToListenAddress == True:
        return config.serverListenAddress

    answer = dns.resolver.resolve_at(where=config.clientDnsResolver, qname=config.clientDnsRecord, rdtype=config.clientDnsRecordType)
    currentIpAddress = answer[0].to_text()
    return currentIpAddress
