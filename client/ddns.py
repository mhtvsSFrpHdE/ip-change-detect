import CloudFlare    # nopep8
import config    # nopep8
import custom_exception    # nopep8

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
        putResult = cf.zones.dns_records.put(zoneId, dnsRecordId, data=newDnsRecord)
    except Exception as e:
        cloudFlareException = custom_exception.CloudFlareException()
        cloudFlareException.rawException = e
        raise cloudFlareException
