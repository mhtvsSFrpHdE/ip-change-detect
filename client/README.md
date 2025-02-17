## From offline to online
The dnspython module cache system default DNS server configuration  
If module process start in offline, then no system default DNS server will be available  
It will cache 0 default DNS server

After internet is online, call `dns.resolver.reset_default_resolver()`   
before send DNS request

Common case: `dns.resolver.resolve_at`, pass argument where as domain instead of IP address  
dnspython will use system default DNS server to find address pass to where
