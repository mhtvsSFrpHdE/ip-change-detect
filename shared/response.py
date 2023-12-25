import config as _config
import random as _random
import string as _string
import json as _json


class Response:
    def __init__(self, auto=True):
        if auto:
            self.serverName = _config.serverName
            self.serverVersion = _config.serverVersion
            # random.choice return single random character
            # then combine with generator expression of string.join to random certain times
            # to get certain length of random string
            self.serverIdentity = ''.join(_random.choice(
                _string.ascii_letters + _string.digits) for _ in range(_config.serverIdentityLength))
            self.presharedKey = _config.presharedKey

    @staticmethod
    def fromJson(jsonString):
        jsonObject = _json.loads(jsonString)

        response = Response(auto=False)
        response.serverName = jsonObject['serverName']
        response.serverVersion = jsonObject['serverVersion']
        response.serverIdentity = jsonObject['serverIdentity']
        response.presharedKey = jsonObject['presharedKey']

        return response

    def toJson(self):
        return _json.dumps(self, default=lambda o: o.__dict__)
