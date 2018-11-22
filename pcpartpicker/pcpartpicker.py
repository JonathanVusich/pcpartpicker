import asyncio
import time
from .scraper import Scraper
from .errors import UnsupportedRegion, UnsupportedPart
from .parser import Parser
from .parts import *

class API:

    _supported_parts = ["cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                        "video-card", "power-supply", "case", "case-fan", "fan-controller",
                        "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                        "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                        "keyboard", "mouse", "speakers", "ups"]
    _regions = ["au", "be", "ca", "de", "es", "fr", "se",
                    "in", "ie", "it", "nz", "uk", "us"]
    _region = "us"
    _parser = None
    _last_refresh = None

    def __init__(self, region: str="us"):
        self._scraper = Scraper(self.region)
        self._parser = Parser()
        self._set_region(region)
        self._last_refresh = time.time()

    @property
    def regions(self):
        return self._regions

    @property
    def supported_parts(self):
        return self._supported_parts

    @property
    def region(self):
        return self._region

    def set_region(self, region: str):
        self._set_region(region)

    def search_part(self, param: str):
        pass

    def retrieve(self, part: str, force_refresh=False):

        # Check part validity
        if part not in self.supported_parts:
            raise UnsupportedPart(f"Part '{part}' is not supported!")

        # Determine whether or not a refresh of the part data should occur
        if hasattr(self, self._parser._part_class_mappings[part].__name__.lower()):
            if time.time() - self._last_refresh < 600 and not force_refresh:
                return getattr(self, part)

        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(self._scraper._retrieve_part(loop, part))
        loop.close()
        results_to_return = []
        for data in results:
            parsed_data = self._parser._parse(part, data)
            if parsed_data:
                results_to_return.extend(parsed_data)
        if results_to_return:
            setattr(self, type(results_to_return[0]).__name__.lower(), results_to_return)
            self._last_refresh = time.time()
            return results_to_return

    def retrieve_all(self, force_refresh=False):
        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(self._scraper._retrieve_all(loop, self.supported_parts))
        loop.close()
        results_to_return = {}
        for part, data_list in zip(self.supported_parts, results):
            results = []
            for data in data_list:
                results.extend(self._parser._parse(part, data))
            if results:
                results_to_return[part] = results
                setattr(self, type(results[0]).__name__.lower(), results)
        if results_to_return:
            self._last_refresh = time.time()
            return results_to_return

    def load_data(self):
        pass

    def dump_data(self):
        pass

    def _set_region(self, region: str):
        if not region in self._regions:
            raise UnsupportedRegion("Region \'{}\' is not supported!".format(region))
        self._region = region
        self._scraper._update_region(self._region)
        self._parser._update_region(self._region)
