import CloudFlare    # nopep8
import time    # nopep8
import subprocess    # nopep8

import config    # nopep8
import custom_exception    # nopep8
import dns_resolver    # nopep8
import log    # nopep8
import internet_alive    # nopep8

from subprocess import check_output    # nopep8

def updateDnsRecord(targetAddress):
    if config.clientIPv6Mode == False:
        cf = CloudFlare.CloudFlare(token=config.clientCloudflareApiToken)

        zones = cf.zones.get(params={'name':config.clientCloudflareZoneName})
        zone = zones[0]
        zoneId = zone['id']

        allDnsRecords = cf.zones.dns_records.get(zoneId, params={'name':config.clientDnsRecord})
        targetDnsRecord = None
        for dnsRecord in allDnsRecords:
            if dnsRecord['type'] == 'A':
                targetDnsRecord = dnsRecord
                break

        newDnsRecord = {
            'name':targetDnsRecord['name'],
            'type':targetDnsRecord['type'],
            'ttl':targetDnsRecord['ttl'],
            'content':targetAddress
        }
        cf.zones.dns_records.put(zoneId, targetDnsRecord['id'], data=newDnsRecord)
    if config.clientIPv6Mode == True:
        cf = CloudFlare.CloudFlare(token=config.clientCloudflareApiToken)

        zones = cf.zones.get(params={'name':config.clientCloudflareZoneName})
        zone = zones[0]
        zoneId = zone['id']

        allDnsRecords = cf.zones.dns_records.get(zoneId, params={'name':config.clientDnsRecord6})
        targetDnsRecord = None
        for dnsRecord in allDnsRecords:
            if dnsRecord['type'] == 'AAAA':
                targetDnsRecord = dnsRecord
                break

        newDnsRecord = {
            'name':targetDnsRecord['name'],
            'type':targetDnsRecord['type'],
            'ttl':targetDnsRecord['ttl'],
            'content':targetAddress
        }
        cf.zones.dns_records.put(zoneId, targetDnsRecord['id'], data=newDnsRecord)

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
            currentExternalIpAddress = None
            rawIpconfigOutput = check_output(["cmd", "/c", "chcp 437 > nul && ipconfig"], universal_newlines=True)
            rawTargetInterface = []
            targetInterfaceDiscovered = False
            for line in rawIpconfigOutput.splitlines():
                if targetInterfaceDiscovered == False:
                    isTargetInterface = line.endswith(config.clientInterfaceName6 + ":")
                    if isTargetInterface:
                        targetInterfaceDiscovered = True
                        continue
                if targetInterfaceDiscovered == True:
                    isAnotherInterface = ("adapter" in line) and line.endswith(":")
                    if (isAnotherInterface):
                        break
                    rawTargetInterface.append(line)
            for line in rawTargetInterface:
                if line.startswith("   IPv6 Address"):
                    addressSection = line.split(':', 1)
                    addressSection = addressSection[1].strip()
                    isPrivateAddress = addressSection.startswith("fd")
                    if isPrivateAddress == False:
                        currentExternalIpAddress = addressSection
                        break
            if currentExternalIpAddress is None:
                log.printToLog(f"Can't get current external IP address from interface: {config.clientInterfaceName6}")
                raise custom_exception.UnknownException()

            currentDnsRecord = dns_resolver.getCurrentDnsRecord()
            log.printToLog(f'Current external IP address: {currentExternalIpAddress}')
            log.printToLog(f'Current DNS record: {currentDnsRecord}')
            if currentDnsRecord == currentExternalIpAddress:
                log.printToLog(f'DNS record does not need to be updated')
                return

            updateDnsRecord(currentExternalIpAddress)
            log.printToLog(f'DNS record has updated to: {currentExternalIpAddress}')

            time.sleep(config.clientCloudflareApiSumbitDelay)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
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
