import dns.resolver    # nopep8

import config    # nopep8

def getExternalIpAddress():
    # Specify IPv4 dns server address here, by default resolver1.opendns.com resolve to IPv6 OpenDNS server
    # And will return only IPv6 record, IPv4 record is dns.resolver.NoAnswer
    # where="resolver1.opendns.com" IPv4 record
    ns1 = "208.67.222.222"
    ns2 = "208.67.220.220"
    try:
        answer = dns.resolver.resolve_at(where=ns1, qname="myip.opendns.com", rdtype="A")
        externalIpAddress = answer[0].to_text()
        return externalIpAddress
    # Ignore first fail
    except dns.exception.DNSException:
        pass

    answer = dns.resolver.resolve_at(where=ns2, qname="myip.opendns.com", rdtype="A")
    externalIpAddress = answer[0].to_text()
    return externalIpAddress

def getCurrentDnsRecord():
    if config.clientIPv6Mode == False:
        if config.debugClientConnectToListenAddress == True:
            return config.serverListenAddress

        answer = dns.resolver.resolve_at(where=config.clientDnsResolver, qname=config.clientDnsRecord, rdtype="A")
        currentIpAddress = answer[0].to_text()
        return currentIpAddress
    if config.clientIPv6Mode == True:
        answer = dns.resolver.resolve_at(where=config.clientDnsResolver, qname=config.clientDnsRecord6, rdtype="AAAA")
        currentIpAddress = answer[0].to_text()
        return currentIpAddress
