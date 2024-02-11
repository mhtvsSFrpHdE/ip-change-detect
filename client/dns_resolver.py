import dns.resolver
import dns.rdatatype

def getExternalIpAddress():
    answer = dns.resolver.resolve_at(where="resolver1.opendns.com", qname="myip.opendns.com", rdtype=dns.rdatatype.A)
    externalIpAddress = answer[0].to_text()
    return externalIpAddress

def getCurrentDnsRecord(where, qname):
    answer = dns.resolver.resolve_at(where=where, qname=qname, rdtype=dns.rdatatype.A)
    currentIpAddress = answer[0].to_text()
    return currentIpAddress
