import dns.resolver    # nopep8
from dns.resolver import NoNameservers    # nopep8
import config    # nopep8

def getExternalIpAddress():
    answer = dns.resolver.resolve_at(where="resolver1.opendns.com", qname="myip.opendns.com", rdtype=config.dnsRecordType)
    externalIpAddress = answer[0].to_text()
    return externalIpAddress

def getCurrentDnsRecord(where, qname):
    answer = dns.resolver.resolve_at(where=where, qname=qname, rdtype=config.dnsRecordType)
    currentIpAddress = answer[0].to_text()
    return currentIpAddress
