# ip-change-detect
## What is this
A open source external IP change detect tool, mainly used for dynamic DNS.  
Compared to commercial solution, this tool doesn't put availability to third party servers.

There are many DDNS project out there but they lack of detect address change,  
mainly rely on polling, which is can be waste if interval too short,  
or delay if interval too big.  
Also they bound to certain provider make them not portable.

## How to use
- Download whole release and extract
- Create python venv enviromnent
- Update pip of venv
- Run `python -m pip install -r requirements.txt` inside venv
- Edit `shared\config.py`
- Run `startup.bat` for IPv4
- Run `startup6.bat` for IPv6
- Install [slaac-watchdog](https://github.com/mhtvsSFrpHdE/slaac-watchdog) if use built-in IPv6 DDNS

After client is connected, your DDNS is set, otherwise you can get notified with  
`IPv6 external action` on external IP changed.

## Expermental IPv6 support
Currently external address detect of built-in DDNS support only Windows.  
Use third party tools for IPv6 DDNS.

## Behind
This program use server listen on port and connect to the port to go through IPv4 NAT.  
If connection dead, consider external IPv4 address is changed,  
update DDNS until next connection can be established.

For IPv6, you need [slaac-watchdog](https://github.com/mhtvsSFrpHdE/slaac-watchdog) to remove old address  
so terminate established IPv6 connection for detect an address change.
