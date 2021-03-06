import struct

import redis
from Jumpscale import j

from ..ZDBClientBase import ZDBClientBase


MODE = "seq"

class ZDBClientSeqMode(ZDBClientBase):

    def _key_encode(self, key):
        if key is None:
            key = ""
        else:
            key = struct.pack("<I", key)
        return key

    def _key_decode(self, key):
        return struct.unpack("<I", key)[0]

    def set(self, data, key=None):
        key1 = self._key_encode(key)
        res = self.redis.execute_command("SET", key1, data)
        if not res:  # data already present, 0-db did nothing.
            return res

        key = self._key_decode(res)
        return key

    def delete(self, key):
        key1 = self._key_encode(key)
        self.redis.execute_command("DEL", key1)

    def get(self, key):
        key = self._key_encode(key)
        return self.redis.execute_command("GET", key)

    def exists(self, key):
        key = self._key_encode(key)
        return self.redis.execute_command("EXISTS", key) == 1
