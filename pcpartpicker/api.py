import logging
from typing import Set, Dict, List

from .handler import Handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class API:
    """API:

    This class is a wrapper class that allows for greater decoupling between
    the internals and the externally available functions.
    """

    def __init__(self, region: str = "us", multithreading=False) -> None:
        self._handler = Handler(region, multithreading=multithreading)

    @property
    def multithreading(self) -> bool:
        return self._handler.multithreading

    @property
    def supported_regions(self) -> Set[str]:
        return self._handler.supported_regions

    @property
    def supported_parts(self) -> Set[str]:
        return self._handler.supported_parts

    @property
    def region(self) -> str:
        return self._handler.region

    def set_region(self, region: str) -> None:
        """
        Public function that allows the user to change the region from which data will be fetched.

        :param region: str: The region
        :return: None
        """

        self._handler.set_region(region)
        logger.debug(f"Region set to {self.region}")

    def set_multithreading(self, multithreading: bool) -> None:
        """
        Function that allows the user to determine whether the scraped HTML is parsed using multiple threads or not.
        Single threading is especially useful for debugging purposes.
        :param multithreading:
        :return:
        """
        self._handler.set_multithreading(multithreading)
        logger.debug(f"Multithreading set to {self.multithreading}")

    def retrieve(self, *args, force_refresh: bool = False) -> Dict[str, List]:
        """
        Public function that allows the user to make part requests.

        :param args: str: Various string arguments that must be valid part types.
        :param force_refresh: bool: This value determines whether or not the API will used internally
        cached values (if available) or freshly acquired data.
        :return: dict: A dictionary that contains the requested parts as keys to their associated data object
        lists.
        """
        logger.debug(f"Retrieving {args}...")
        return self._handler.retrieve(*args, force_refresh=force_refresh)

    def retrieve_all(self, force_refresh: bool = False) -> Dict[str, List]:
        """
        Public function that allows the user to retrieve all supported part types.

        :param force_refresh: bool: This value determines whether or not the API will used internally
        cached values (if available) or freshly acquired data.
        :return: dict: A dictionary that contains all parts as keys to their associated data object
        lists.
        """
        logger.debug(f"Retrieving all parts...")
        return self._handler.retrieve(*self._handler.supported_parts, force_refresh=force_refresh)
