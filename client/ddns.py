import CloudFlare    # nopep8
import time    # nopep8
import subprocess    # nopep8

import config    # nopep8
import custom_exception    # nopep8
import dns_resolver    # nopep8
import log    # nopep8
import internet_alive    # nopep8

def updateDnsRecord(targetAddress):
    try:
        cf = CloudFlare.CloudFlare(token=config.clientCloudflareApiToken)

        zones = cf.zones.get(params={'name':config.clientCloudflareZoneName})
        zone = zones[0]
        zoneId = zone['id']

        dnsRecords = cf.zones.dns_records.get(zoneId, params={'name':config.clientDnsRecord})
        dnsRecord = dnsRecords[0]
        dnsRecordId = dnsRecord['id']

        newDnsRecord = {
            'name':dnsRecord['name'],
            'type':dnsRecord['type'],
            'content':targetAddress
        }
        cf.zones.dns_records.put(zoneId, dnsRecordId, data=newDnsRecord)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        try:
            internet_alive.testInternet()
        except custom_exception.InternetOfflineException as internetOfflineException:
            raise internetOfflineException

        cloudFlareException = custom_exception.CloudFlareException()
        cloudFlareException.rawException = e
        raise cloudFlareException

def ddnsMain():
    if (config.clientUseCloudflare == False):
        log.printToLog('Update DDNS through external action')
        process = subprocess.Popen(config.clientExternalActionOnIpChange, shell=True)
        process.wait()
        log.printToLog(f'External action return code: {process.returncode}')
        return

    currentExternalIpAddress = dns_resolver.getExternalIpAddress()
    currentDnsRecord = dns_resolver.getCurrentDnsRecord()
    log.printToLog(f'Current external IP address: {currentExternalIpAddress}')
    log.printToLog(f'Current DNS record: {currentDnsRecord}')
    if currentDnsRecord == currentExternalIpAddress:
        log.printToLog(f'DNS record does not need to be updated')
        return

    updateDnsRecord(currentExternalIpAddress)
    log.printToLog(f'DNS record has updated to: {currentExternalIpAddress}')

    time.sleep(config.clientCloudflareApiSumbitDelay)
