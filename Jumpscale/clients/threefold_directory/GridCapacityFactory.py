# DO NOT EDIT THIS FILE. This file will be overwritten when re-running go-raml.
from Jumpscale import j

from .api_service import ApiService

from .http_client import HTTPClient

JSConfigClient = j.application.JSBaseConfigClass
JSConfigs = j.application.JSBaseConfigsClass


class Client(JSConfigClient):
    _SCHEMATEXT = """
    @url = jumpscale.threefold_directory.client
    name* = "" (S)
    base_uri = "https://capacity.threefoldtoken.com" (S)
    """

    def _init(self):
        http_client = HTTPClient(self.base_uri)
        self.api = ApiService(http_client)
        self.close = http_client.close


class GridCapacityFactory(JSConfigs):
    __jslocation__ = "j.clients.threefold_directory"
    _CHILDCLASS = Client

    def _init(self):
        self.connections = {}
        self._api = None

    @property
    def client(self):
        if self._api is None:
            self.get(name="main")
            self._api = self.get().api
        return self._api

    @property
    def _capacity(self):
        def do():
            return [item for item in self.client.ListCapacity()[0]]
        return self._cache.get("_capacity", method=do, expire=600)

    @property
    def _farmers(self):
        def do():
            return [item for item in self.client.ListFarmers()[0]]
        return self._cache.get("_farmers", method=do, expire=600)

    @property
    def capacity(self):
        """
        is cached for 60 sec
        """
        return [item.as_dict() for item in self._capacity]

    @property
    def farmers(self):
        """
        is cached for 60 sec
        """
        return [item.as_dict() for item in self._farmers]

    def resource_units(self, reload=False):
        """
        js_shell "print(j.clients.threefold_directory.resource_units())"
        """
        if reload:
            self._cache.reset()
        nodes = self._capacity

        resource_units = {
            'cru': 0,
            'mru': 0,
            'hru': 0,
            'sru': 0,
        }

        for node in nodes:
            resource_units['cru'] += node.total_resources.cru
            resource_units['mru'] += node.total_resources.mru
            resource_units['hru'] += node.total_resources.hru
            resource_units['sru'] += node.total_resources.sru

        return(resource_units)
