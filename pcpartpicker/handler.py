import asyncio
import logging
import multiprocessing
import time
from typing import List, Tuple, Set, Dict

from .errors import UnsupportedRegion, UnsupportedPart
from .mappings import part_classes
from .parser import Parser
from .scraper import Scraper

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class Handler:
    _supported_parts: Set[str] = {"cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                                  "video-card", "power-supply", "case", "case-fan", "fan-controller",
                                  "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                                  "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                                  "keyboard", "mouse", "speakers", "ups"}

    _supported_regions: Set[str] = {"au", "be", "ca", "de", "es", "fr", "se",
                                    "in", "ie", "it", "nz", "uk", "us"}

    _region: str = "us"
    _last_refresh: float = None
    _concurrent_connections: int = 25
    _multithreading: bool = True
    _scraper: Scraper = None
    _parser: Parser = None

    def __init__(self, region: str = "us", concurrent_connections: int = 25, multithreading: bool = True) -> None:
        if region not in self._supported_regions:
            raise UnsupportedRegion(f"Region '{region}' is not supported for this API!")
        self._region = region
        self._last_refresh = time.time()
        self._multithreading = multithreading
        self._concurrent_connections = concurrent_connections
        self._scraper = Scraper(self.region, concurrent_connections=concurrent_connections)
        self._parser = Parser(self.region)

    @property
    def region(self) -> str:
        return self._region

    @property
    def supported_parts(self) -> Set[str]:
        return self._supported_parts

    @property
    def supported_regions(self) -> Set[str]:
        return self._supported_regions

    @property
    def concurrent_connections(self) -> int:
        return self._concurrent_connections

    @property
    def multithreading(self) -> bool:
        return self._multithreading

    def set_region(self, region: str) -> None:
        """
        Hidden method that changes the region for the parser and scraper objects contained in this instance.

        :param region: str: New region
        :return: None
        """
        if region not in self._supported_regions:
            raise UnsupportedRegion(f"Region '{region}' is not supported for this API!")
        self._region = region
        self._scraper = Scraper(region, concurrent_connections=self._concurrent_connections)
        self._parser = Parser(region)

    def set_concurrent_connections(self, concurrent_connections: int) -> None:
        """
        Function that allows the user to set how many concurrent connections should be opened
        to PCPartPicker.com. Higher values are more prone to cause timeout failures, while low
        values increase the time needed to collect results.
        :param concurrent_connections:
        :return:
        """
        self._concurrent_connections = concurrent_connections
        self._scraper = Scraper(self.region, concurrent_connections=self._concurrent_connections)

    def set_multithreading(self, multithreading: bool) -> None:
        """
        Function that allows the user to specify whether or not the API should run multithreaded or not.
        Multithreading allows for easier debugging of the internals but also greatly amplifies the amount
        of time necessary to process all of the retrieved data.
        :param multithreading:
        :return:
        """
        self._multithreading = multithreading

    def retrieve(self, *args, force_refresh=False):
        """
        Hidden function that is designed to retrieve and parse part data from PCPartPicker.

        :param args: str: Variable number of arguments that must map to valid parts.
        :param force_refresh: bool: This value determines whether or not to completely refresh the
        entire API database, or to simply retrieve cached values.
        :return: dict: A dictionary of the input part types with their mapped data object values.
        """
        results: Dict[str, List] = {}

        # Verify the validity of the parts
        for part in args:
            if part not in self._supported_parts:
                raise UnsupportedPart(f"Part '{part}' is not supported by this API!")

        # Determine whether or not a refresh of part data should occur
        for part in args:
            if hasattr(self, f"{part_classes[part].__name__.lower()}_{self._region}"):
                if time.time() - self._last_refresh < 600 and not force_refresh:
                    logger.debug(f"Retrieving cached data for {part}...")
                    results[part] = getattr(self, f"{part_classes[part].__name__.lower()}_{self._region}")

        if len(results) == len(args):
            logger.debug(f"All parts were cached.")
            return results

        parts_to_download: List[str] = [part for part in args if part not in results]

        logger.debug(f"Downloading html for {parts_to_download}...")

        start = time.perf_counter()
        loop = asyncio.get_event_loop()
        html: List[Tuple[str, List[str]]] = loop.run_until_complete(self._scraper.retrieve(parts_to_download))
        total_time = time.perf_counter() - start

        logger.debug(f"Completed downloading! Time elapsed is {total_time} seconds.")

        start = time.perf_counter()
        if self._multithreading:
            logger.debug(f"Parsing with multiple threads...")
            pool = multiprocessing.Pool()
            parsed_objects = pool.map(self._parser.parse, html)
        else:
            logger.debug(f"Parsing with one thread...")
            parsed_objects = [self._parser.parse(page) for page in html]
        total_time = time.perf_counter() - start

        logger.debug(f"Completed parsing! Time elapsed is {total_time} seconds.")

        for part, data in parsed_objects:
            setattr(self, f"{part_classes[part].__name__.lower()}_{self._region}", data)
            results[part] = data
        return results
