from Jumpscale import j


class RedisConfig(j.application.JSBaseConfigClass):

    _SCHEMATEXT = """
    @url = jumpscale.redis_config.client
    name* = "" (S)
    addr = "127.0.0.1" (ipaddr)
    port = 6379 (ipport)
    password_ = "" (S)
    ardb_patch = false (B)
    unixsocket = "" (S)
    set_patch = false (B)
    ssl = false (B)
    sslkey = false (B)
    ssl_keypath = "" (S)
    """

    def _init(self):
        self._redis = None

    @property
    def ssl_certfile_path(self):
        '''
        :return: ssl_certificate file path
        :rtype: str
        '''

        p = j.sal.fs.getDirName(self.ssl_keypath) + "cert.pem"
        if self.sslkey:
            return p

    @property
    def ssl_keyfile_path(self):
        '''
        :return: ssl_key file path
        :rtype: str
        '''

        p = j.sal.fs.getDirName(self.ssl_keypath) + "key.pem"
        if self.sslkey:
            return p

    @property
    def redis(self):
        if self._redis is None:

            if self.unixsocket == "":
                self.unixsocket = None

            if self.ssl:
                self._redis = j.clients.redis.get(
                    ipaddr=self.addr, port=self.port, password=self.password_,
                    unixsocket=self.unixsocket, ardb_patch=self.ardb_patch,
                    set_patch=self.set_patch, ssl=self.ssl,
                    ssl_keyfile=self.ssl_keyfile_path, ssl_certfile=self.ssl_certfile_path,
                    ssl_cert_reqs=None, ssl_ca_certs=None)
            else:
                self._redis = j.clients.redis.get(
                    ipaddr=self.addr, port=self.port, password=self.password_,
                    unixsocket=self.unixsocket, ardb_patch=self.ardb_patch,
                    set_patch=self.set_patch, ssl=self.ssl,
                    ssl_cert_reqs=None, ssl_ca_certs=None)

        return self._redis

    def ssl_keys_save(self, ssl_keyfile, ssl_certfile):
        '''
        :param ssl_keyfile: ssl_key file path
        :type ssl_keyfile: str
        :param ssl_certfile: ssl_certificate
        :type ssl_certfile: str
        '''

        if j.sal.fs.exists(ssl_keyfile):
            ssl_keyfile = j.sal.fs.readFile(ssl_keyfile)
        if j.sal.fs.exists(ssl_certfile):
            ssl_certfile = j.sal.fs.readFile(ssl_certfile)
        j.sal.fs.writeFile(self.ssl_certfile_path, ssl_certfile)
        j.sal.fs.writeFile(self.ssl_keyfile_path, ssl_keyfile)

    def __str__(self):
        return "redis:%-14s %-25s:%-4s (ssl:%s)" % (self.name, self.addr, self.port, self.ssl)

    __repr__ = __str__
