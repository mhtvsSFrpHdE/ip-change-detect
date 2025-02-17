import sys    # nopep8
import json    # nopep8

import config    # nopep8
import log    # nopep8
import custom_exception    # nopep8

from subprocess import check_output    # nopep8

def get_ip():
    currentExternalIpAddress = None

    if sys.platform.startswith('win32'):
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
    elif sys.platform.startswith('linux'):
        rawIpconfigOutput = check_output(["ip", "--json", "addr"], universal_newlines=True)
        ipOutputInJson = json.loads(rawIpconfigOutput)
        for interface in ipOutputInJson:
            if interface["ifname"] == config.clientInterfaceName6:
                for ip in interface["addr_info"]:
                    if ip["family"] == "inet6":
                        if "dynamic" in ip and "temporary" not in ip:
                            currentExternalIpAddress = ip["local"]
                            break
                break

    if currentExternalIpAddress is None:
        log.printToLog(f"Can't get current external IP address from interface: {config.clientInterfaceName6}")
        raise custom_exception.UnknownException()

    return currentExternalIpAddress
