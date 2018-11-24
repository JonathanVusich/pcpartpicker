import asyncio
import time
import multiprocessing
from .scraper import Scraper
from .parser import Parser
from .errors import UnsupportedRegion, UnsupportedPart


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

    def __init__(self, region: str="us"):
        if region not in self._regions:
            raise UnsupportedRegion(f"Region '{region}' is not supported for this API!")
        self._region = region
        self._scraper = Scraper(self.region)
        self._parser = Parser(self.region)
        self._last_refresh = time.time()

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
        self._scraper._set_region(region)
        self._parser._set_region(region)

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
            if hasattr(self, self._parser._part_class_mappings[part].__name__.lower()):
                if time.time() - self._last_refresh < 600 and not force_refresh:
                    results[part] = getattr(self, part)

        if len(results) == len(args):
            return results

        parts_to_download = [part for part in args if not part in results]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        html = loop.run_until_complete(self._scraper._retrieve(loop, *parts_to_download))
        loop.close()

        args = list(zip(parts_to_download, html))

        pool = multiprocessing.Pool()
        parsed_objects = pool.map(self._parser._parse, args)
        for part, data in parsed_objects:
            setattr(self, part, data)
            results[part] = data
        return results