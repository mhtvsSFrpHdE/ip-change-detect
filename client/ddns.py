import CloudFlare    # nopep8
import config    # nopep8
import custom_exception    # nopep8
import dns_resolver    # nopep8

def updateDnsRecord(targetAddress):
    try:
        cf = CloudFlare.CloudFlare(token=config.cloudflareApiToken)

        zones = cf.zones.get(params={'name':config.cloudflareZoneName})
        zone = zones[0]
        zoneId = zone['id']

        dnsRecords = cf.zones.dns_records.get(zoneId, params={'name':config.dnsRecord})
        dnsRecord = dnsRecords[0]
        dnsRecordId = dnsRecord['id']

        newDnsRecord = {
            'name':dnsRecord['name'],
            'type':dnsRecord['type'],
            'content':targetAddress
        }
        cf.zones.dns_records.put(zoneId, dnsRecordId, data=newDnsRecord)
    except Exception as e:
        cloudFlareException = custom_exception.CloudFlareException()
        cloudFlareException.rawException = e
        raise cloudFlareException

def ddnsMain():
    currentExternalIpAddress = dns_resolver.getExternalIpAddress()
    currentDnsRecord = dns_resolver.getCurrentDnsRecord()
    print(f'Current external IP address: {currentExternalIpAddress}')
    print(f'Current DNS record: {currentDnsRecord}')
    if currentDnsRecord == currentExternalIpAddress:
        print(f'DNS record does not need to be updated')
        return

    updateDnsRecord(currentExternalIpAddress)
    print(f'DNS record has updated to: {currentExternalIpAddress}')
