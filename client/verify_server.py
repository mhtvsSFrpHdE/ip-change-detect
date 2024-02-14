from response import Response    # nopep8

response = Response()

knownServerVersion = response.serverVersion
# Allow to update server identity if preshared key is match
knownServerIdentity = None
knownPresharedKey = response.presharedKey
serverInformationRecorded = False
