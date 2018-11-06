import asyncio
import time
from .scraper import Scraper
from .errors import UnsupportedRegion

class API:

    _supported_types = ["cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                        "video-card", "power-supply", "case", "case-fan", "fan-controller",
                        "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                        "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                        "keyboard", "mouse", "speakers", "ups"]
    _regions = ["au", "be", "ca", "de", "es", "fr",
                    "in", "ie", "it", "nz", "uk", "us"]
    _region = "us"
    _database = None

    def __init__(self, region: str="us"):
        self._set_region(region)
        self._scraper = Scraper(self.region)

    @property
    def regions(self):
        return self._regions

    @property
    def supported_types(self):
        return self._supported_types

    @property
    def region(self):
        return self._region

    def set_region(self, region: str):
        self._set_region(region)

    def search_part(self, param: str):
        pass

    def retrieve(self, type: str):
        pass

    def retrieve_all(self):
        loop = asyncio.get_event_loop()
        start = time.perf_counter()
        results = loop.run_until_complete(self._scraper._retrieve_all(loop))
        print(time.perf_counter() - start)
        loop.close()

    def load_data(self):
        pass

    def dump_data(self):
        pass

    def _set_region(self, region: str):
        if not region in self._regions:
            raise UnsupportedRegion("Region \'{}\' is not supported!".format(region))
        self._region = region
