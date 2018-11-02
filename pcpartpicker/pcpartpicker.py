import asyncio
import requests

class API:

    _supported_types = ["cpu"]
    _regions = ["au", "be", "ca", "de", "es", "fr",
                    "in", "ie", "it", "nz", "uk", "us"]
    _region = "us"

    @property
    def regions(self):
        return self._regions

    @property
    def supported_types(self):
        return self._supported_types

    @property
    def region(self):
        return self._region

    def __init__(self, region="us"):
        self._set_region(region)

    def _set_region(self, region):
        if not region in self._regions:
            raise UnsupportedRegion("Region {} is not supported!".format(region))
        self._region = region

    def set_region(region: str):
        self._set_region(region)

    def search_part(param: str):
        pass

    def retrieve_type(type: str):
        pass

    def retrieve_all():
        pass

    def load_data():
        pass

    def dump_data():
        pass


class UnsupportedRegion(Exception):
    pass
