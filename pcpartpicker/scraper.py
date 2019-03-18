import asyncio
from typing import List, Tuple, Iterable
import logging
import concurrent.futures

import aiohttp

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class Scraper:
    """Scraper:

    This class is designed to retrieve http requests in a fast and efficient manner.

    Attributes:
        _region: str:
            This variable holds the region that is used to build URLs for PCPartPicker.
        _base_url: str:
            This variable holds the product URL from which the actual request URLs are built.

    """

    _region: str = "us"
    _base_url: str = None
    _concurrent_connections: int = None

    def __init__(self, region: str = "us", concurrent_connections: int = 25) -> None:
        self._region = region
        self._concurrent_connections = concurrent_connections
        self._base_url = self._generate_base_url()

    def _generate_base_url(self) -> str:
        """
        Hidden method that is used to generate the base URL for regional requests.

        :return: str: Represents the base URL for regional requests.
        """

        if not self._region == "us":
            return "https://{}.pcpartpicker.com/products/".format(self._region)
        return "https://pcpartpicker.com/products/"

    def _generate_product_url(self, part: str, page_num: int = 1) -> str:
        """
        Hidden method that is used to generate specific URLs for products.
        Relies on the base URL for generation.

        :param part: str: Represents the part data to retrieve.
        :param page_num: Represents the page number to retrieve.
        :return: str: The URL that represents the specific page for the given part.
        """

        return "{}{}/fetch?page={}".format(self._base_url, part, page_num)

    async def _retrieve_page_numbers(self, session: aiohttp.ClientSession, part: str) -> List[int]:
        """
        Hidden method that retrieves a list of page numbers for a given part type.

        :param session: aiohttp.ClientSession: The asynchronous session used for making requests.
        :param part: str: The part type.
        :return: list: A list of numbers that represents the different page numbers of the given part type.
        """

        data: dict = await self._retrieve_page_data(session, part)
        num = data["result"]["paging_data"]["page_blocks"][-1]["page"]
        return [x for x in range(1, num + 1)]

    async def _retrieve_page_data(self, session: aiohttp.ClientSession, part: str, page_num: int = 1) -> str:
        """
        Hidden method that retrieves page data for a given part type and page number.

        :param session: aiohttp.ClientSession: The asynchronous session used for making requests.
        :param part: str: The part type.
        :param page_num: int: The page number.
        :return: str: The raw page data for this request.
        """

        async with session.get(self._generate_product_url(part, page_num)) as page:
            return await page.json(content_type=None)

    async def _retrieve_part_data(self, session: aiohttp.ClientSession, part: str) -> List[List[str]]:
        """
        Hidden method that returns a list of raw page data for a given part.

        :param session: aiohttp.ClientSession: The asynchronous session that is used to generate requests.
        :param part: str: The part type to retrieve.
        :return: list: A list of raw page data for the given part.
        """

        page_numbers = await self._retrieve_page_numbers(session, part)
        tasks = [self._retrieve_page_data(session, part, num) for num in page_numbers]
        return await asyncio.gather(*tasks)

    async def retrieve(self, args: Iterable[str]) -> List[Tuple[str, List[str]]]:
        """
        Hidden method that returns a list of lists of JSON page data.

        :param args: Various part types that are used to make the requests.
        :return: list: A list of lists of JSON page data.
        """

        parts = [arg for arg in args]
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=self._concurrent_connections, ttl_dns_cache=300)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [self._retrieve_part_data(session, part) for part in args]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            retry_parts = []
            for part, result in zip(parts, results):
                if isinstance(result, concurrent.futures.TimeoutError):
                    logger.error(f"{part} timed out! Retrying...")
                    retry_parts.append(part)
                elif isinstance(result, Exception):
                    raise result
            if retry_parts:
                results.append(await self.retrieve(retry_parts))

            part_data: List[Tuple[str, List[str]]] = []
            for part, result in zip(parts, results):
                html_data = [page["result"]["html"] for page in result]
                part_data.append((part, html_data))
            return part_data
