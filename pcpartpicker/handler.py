import asyncio
import multiprocessing
import time

from .errors import UnsupportedRegion, UnsupportedPart
from .mappings import part_classes
from .parser import Parser
from .scraper import Scraper


class Handler:
    _supported_parts = {"cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                        "video-card", "power-supply", "case", "case-fan", "fan-controller",
                        "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                        "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                        "keyboard", "mouse", "speakers", "ups"}

    _regions = {"au", "be", "ca", "de", "es", "fr", "se",
                "in", "ie", "it", "nz", "uk", "us"}

    _region = "us"
    _last_refresh = None

    def __init__(self, region: str = "us"):
        if region not in self._regions:
            raise UnsupportedRegion(f"Region '{region}' is not supported for this API!")
        self._region = region
        self._scraper = Scraper(self.region)
        self._parser = Parser(self.region)
        self._last_refresh = time.time()
        self._concurrent_connections = 25

    @property
    def region(self):
        return self._region

    def _set_region(self, region: str):
        """
        Hidden method that changes the region for the parser and scraper objects contained in this instance.

        :param region: str: New region
        :return: None
        """
        if region not in self._regions:
            raise UnsupportedRegion(f"Region '{region}' is not supported for this API!")
        self._region = region
        self._scraper = Scraper(region)
        self._parser = Parser(region)

    def _set_concurrent_connections(self, number: int) -> None:
        """
        Function that allows the user to set how many concurrent connections should be opened
        to PCPartPicker.com. Higher values are more prone to cause timeout failures, while low
        values increase the time needed to collect results.
        :param number:
        :return:
        """
        self._concurrent_connections = number

    def _retrieve(self, *args, force_refresh=False):
        """
        Hidden function that is designed to retrieve and parse part data from PCPartPicker.

        :param args: str: Variable number of arguments that must map to valid parts.
        :param force_refresh: bool: This value determines whether or not to completely refresh the
        entire API database, or to simply retrieve cached values.
        :return: dict: A dictionary of the input part types with their mapped data object values.
        """
        results = {}

        # Verify the validity of the parts
        for part in args:
            if part not in self._supported_parts:
                raise UnsupportedPart(f"Part '{part}' is not supported by this API!")

        # Determine whether or not a refresh of part data should occur
        for part in args:
            if hasattr(self, f"{part_classes[part].__name__.lower()}_{self._region}"):
                if time.time() - self._last_refresh < 600 and not force_refresh:
                    results[part] = getattr(self, f"{part_classes[part].__name__.lower()}_{self._region}")

        if len(results) == len(args):
            return results

        parts_to_download = [part for part in args if part not in results]

        loop = asyncio.get_event_loop()
        html = loop.run_until_complete(self._scraper.retrieve(self._concurrent_connections, *parts_to_download))
        loop.close()

        args = list(zip(parts_to_download, html))

        pool = multiprocessing.Pool()
        parsed_objects = pool.map(self._parser.parse, args)
        for part, data in parsed_objects:
            setattr(self, f"{part_classes[part].__name__.lower()}_{self._region}", data)
            results[part] = data
        return results
