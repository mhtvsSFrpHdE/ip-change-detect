import os    # nopep8
import sys    # nopep8
from argparse import ArgumentParser    # nopep8

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))    # nopep8
import config    # nopep8
import ddns    # nopep8

parser = ArgumentParser()
parser.add_argument('ip_address', help="IP address")
parser.add_argument("-6", "--ipv6", action="store_true", help="Run in IPv6 mode")
args = parser.parse_args()
if (args.ipv6):
    config.clientIPv6Mode = True

ddns.updateDnsRecord(args.ip_address)
