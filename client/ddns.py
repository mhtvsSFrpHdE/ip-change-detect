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
    if config.clientIPv6Mode == True:
        try:
            cf = CloudFlare.CloudFlare(token=config.clientCloudflareApiToken)

            zones = cf.zones.get(params={'name':config.clientCloudflareZoneName})
            zone = zones[0]
            zoneId = zone['id']

            dnsRecords = cf.zones.dns_records.get(zoneId, params={'name':config.clientDnsRecord6})
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
    if config.clientIPv6Mode == False:
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

    if config.clientIPv6Mode == True:
        if (config.clientUseCloudflare == False):
            log.printToLog('Update DDNS through external action')
            process = subprocess.Popen(config.clientExternalActionOnIpChange6, shell=True)
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
