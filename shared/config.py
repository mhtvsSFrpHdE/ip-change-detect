# ===== Password =====

# string, Client use this password to know if connected to expected server
presharedKey = "9IGFWa9hcKmtbh0CNsdj"

# ===== Password =====

# ===== Server config =====

# string, IP address like "192.168.1.100", or "0.0.0.0" to all IP addresses
serverListenAddress = "0.0.0.0"
# Placeholder, use server\main.py -6 or --ipv6 to enable IPv6 mode
serverIPv6Mode = False
# string, IPv6 address if not none, "::" to all IPv6 addresses
serverListenAddress6 = "::"
# int, port number
serverPort = 65432

# int, if client count is more than this number, client will be disconnected
# Usually only 1 client will connect, otherwise you may under DDOS attack
serverMaxConnection = 10

# ===== Server config =====

# ===== Client config =====

# string, Your DNS provider DNS server that has most up to date DNS record
# A third party DNS server has its own DNS cache and the query result can be outdated
# For example, if use cloudflare, dnsResolver is "izabella.ns.cloudflare.com"
clientDnsResolver = None
# string, Your domain A record address like "a.bing.com", client will connect to this address
# if use cloudflare, DNS record will also submit to this address
clientDnsRecord = None
# Placeholder, use client\main.py -6 or --ipv6 to enable IPv6 mode
clientIPv6Mode = False
# Your SLAAC IPv6 address goes here
clientDnsRecord6 = None
# string, specify a DNS server and DNS record here
# This DNS server will be used for internet online test
# Specify a different server than dnsResolver can let you to know
# if it's indeed offline or just DNS provider is down
clientInternetAliveServer = "1.1.1.1"
clientInternetAliveQuery = "bing.com"
# bool, Use cloudflare API to update DNS record and get DDNS
clientUseCloudflare = False
# string, Your cloudflare API token
clientCloudflareApiToken = None
# string, Your cloudflare zone name, usually is your domain root name, "bing.com"
clientCloudflareZoneName = None
# int, After call cloudflare API, wait second before try to continue connect
# DNS record takes few time to be updated
clientCloudflareApiSumbitDelay = 30
# string, If your domain is not use cloudflare DNS
# specify an external command that can update your DDNS
# or anything else
clientExternalActionOnIpChange = "ping.exe 1.1.1.1"

# ===== Client config =====

# ===== Client default value =====

# int, second, timeout when client try to connect
clientSocketTimeout = 3
# int, second, retry interval when client connection failed
clientReconnectInterval = 1
# int, second, max retry count when client connection failed before request DDNS update
clientRetryMaxCountOnDisconnect = 5
# int, second, max retry count when client connect to unknown server (no response)
clientTimeoutMaxCountOnDisconnect = 5
# int, second, max retry count when client connect to unknown server (wrong response)
clientJsonDecodeErrorMaxCountOnDisconnect = 5

# ===== Client default value =====

# ===== Socket default value =====

# int, Socket keepalive settings, if server or client suddenly done
# socket will not shutdown automatically and on both side don't know another side is off
# keepalive packet 60, 0, 0 may test connection is alive each minute
keepaliveAfterIdleSec = 60
keepaliveIntervalSec = 0
keepaliveMaxFails = 0
# int, socket recv argument
socketBufferLength = 1024

# ===== Socket default value =====

# ===== Server information =====

# These are optional variable describe server information
# But they may not actually be used in server identity verification
serverName = "IP change detect"
serverVersion = 0
serverIdentityLength = 20

# ===== Server information =====

# ===== Debug flag =====

# bool, server use same identity in each reboot
debugServerFixIdentity = False
# bool, client connect to serverListenAddress directly instead of get server address from DNS record
debugClientConnectToListenAddress = False

# ===== Debug flag =====

# ===== Log =====

# string, Where to save logs
logFolder = "../logs/<type>"
# string, Server log or client log
logTypePlaceholder="<type>"
# string, Timestamp position in log file name
logTimestampPlaceholder = "<timestamp>"
# string Timestamp format, goes to datetime.now().strftime
logTimestampFormat = "%Y-%m-%d-%H-%M-%S"
# string, Log file name with placeholder
logFileName = "ip-change-detect-<type>-<timestamp>.log"
# string, Server log folder name
logTypeServer = "server"
# string, Client log folder name
logTypeClient = "client"

# ===== Log =====

# ===== Metadata =====

# int, version of config file itself, automatically update config format in future
configVersion = 0

# ===== Metadata =====
