import cloudflare    # nopep8
import time    # nopep8
import subprocess    # nopep8

import config    # nopep8
import custom_exception    # nopep8
import dns_resolver    # nopep8
import log    # nopep8
import internet_alive    # nopep8
import get_interface    # nopep8

def updateDnsRecord(targetAddress):
    if config.clientIPv6Mode == False:
        cf = cloudflare.Cloudflare(api_token=config.clientCloudflareApiToken)

        allDnsRecords = cf.dns.records.list(zone_id=config.clientCloudflareZoneId, name=config.clientDnsRecord)
        targetDnsRecord = None
        for dnsRecord in allDnsRecords:
            if dnsRecord.type == 'A':
                targetDnsRecord = dnsRecord
                break

        cf.dns.records.edit(zone_id=config.clientCloudflareZoneId, dns_record_id=targetDnsRecord.id, content=targetAddress)
    if config.clientIPv6Mode == True:
        cf = cloudflare.Cloudflare(api_token=config.clientCloudflareApiToken)

        allDnsRecords = cf.dns.records.list(zone_id=config.clientCloudflareZoneId, name=config.clientDnsRecord6)
        targetDnsRecord = None
        for dnsRecord in allDnsRecords:
            if dnsRecord.type == 'AAAA':
                targetDnsRecord = dnsRecord
                print(dnsRecord)
                break

        cf.dns.records.edit(zone_id=config.clientCloudflareZoneId, dns_record_id=targetDnsRecord.id, content=targetAddress)

_redundantDdnsAttempts = 0

def ddnsMain():
    global _redundantDdnsAttempts

    try:
        if config.clientIPv6Mode == False:
            if (config.clientUseCloudflare == False):
                log.printToLog('Update DDNS through external action')
                process = subprocess.Popen(config.clientExternalActionOnIpChange)
                process.wait()
                log.printToLog(f'External action return code: {process.returncode}')
                return

            currentExternalIpAddress = dns_resolver.getExternalIpAddress()
            currentDnsRecord = dns_resolver.getCurrentDnsRecord()
            log.printToLog(f'Current external IP address: {currentExternalIpAddress}')
            log.printToLog(f'Current DNS record: {currentDnsRecord}')
            if currentDnsRecord == currentExternalIpAddress:
                _redundantDdnsAttempts = _redundantDdnsAttempts + 1
                log.printToLog(f'DNS record does not need to be updated')

                if (_redundantDdnsAttempts > config.clientMaxRedundantDdnsAttempt):
                    raise custom_exception.RedundantDdnsAttemptsException("External address detection method may not reliable, or server is down")
                return

            _redundantDdnsAttempts = 0
            updateDnsRecord(currentExternalIpAddress)
            log.printToLog(f'DNS record has updated to: {currentExternalIpAddress}')

            time.sleep(config.clientCloudflareApiSumbitDelay)

        if config.clientIPv6Mode == True:
            if (config.clientUseCloudflare == False):
                log.printToLog('Update DDNS through external action')
                process = subprocess.Popen(config.clientExternalActionOnIpChange6)
                process.wait()
                log.printToLog(f'External action return code: {process.returncode}')
                return

            # Get IPv6 address
            currentExternalIpAddress = get_interface.get_ip()

            currentDnsRecord = dns_resolver.getCurrentDnsRecord()
            log.printToLog(f'Current external IP address: {currentExternalIpAddress}')
            log.printToLog(f'Current DNS record: {currentDnsRecord}')
            if currentDnsRecord == currentExternalIpAddress:
                log.printToLog(f'DNS record does not need to be updated')
                return

            updateDnsRecord(currentExternalIpAddress)
            log.printToLog(f'DNS record has updated to: {currentExternalIpAddress}')

            time.sleep(config.clientCloudflareApiSumbitDelay)
    except cloudflare.APIError as e:
        try:
            internet_alive.testInternet()
        except custom_exception.InternetOfflineException as internetOfflineException:
            raise internetOfflineException

        cloudFlareException = custom_exception.DdnsProviderException()
        cloudFlareException.rawException = e
        raise cloudFlareException
    except (dns_resolver.dns.resolver.LifetimeTimeout, dns_resolver.dns.resolver.NoNameservers) as e:
        try:
            internet_alive.testInternet()
        except custom_exception.InternetOfflineException as internetOfflineException:
            raise internetOfflineException

        dnsUnavailableException = custom_exception.DnsResolverException()
        dnsUnavailableException.rawException = e
        raise dnsUnavailableException
