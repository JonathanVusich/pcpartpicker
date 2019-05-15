import asyncio
import json
import logging
from typing import List, Tuple, Iterable, Dict

import aiohttp
import lxml.html

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
        num_data = data["result"]["paging_row"]
        html_tags = lxml.html.fromstring(num_data)
        tags = html_tags.xpath('section/ul/li')
        return [x for x in range(1, len(tags) + 1)]

    async def _retrieve_page_data(self, session: aiohttp.ClientSession, part: str, page_num: int = 1) -> dict:
        """
        Hidden method that retrieves page data for a given part type and page number.

        :param session: aiohttp.ClientSession: The asynchronous session used for making requests.
        :param part: str: The part type.
        :param page_num: int: The page number.
        :return: str: The raw page data for this request.
        """

        while True:
            async with session.get(self._generate_product_url(part, page_num)) as page:
                try:
                    return await page.json(content_type=None)
                except json.JSONDecodeError:
                    logger.debug("PCPartPicker server was overloaded! Sleeping...")
                    await asyncio.sleep(.5)

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

    async def _retrieve_all_part_data(self, args: Iterable[str]) -> Dict[str, List[dict]]:
        parts = [arg for arg in args]
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=self._concurrent_connections, ttl_dns_cache=300)
        final_results = {}
        async with aiohttp.ClientSession(connector=connector, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/39.0.2171.95 Safari/537.36'}) as session:
            tasks = [self._retrieve_part_data(session, part) for part in args]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            retry_parts = []
            for part, result in zip(parts, results):
                if isinstance(result, asyncio.TimeoutError):
                    logger.debug(f"Fetching data for {part} timed out! Retrying...")
                    retry_parts.append(part)
                elif isinstance(result, Exception):
                    raise result
                else:
                    final_results.update({part: result})

            if retry_parts:
                final_results.update(await self._retrieve_all_part_data(retry_parts))
        return final_results

    async def retrieve(self, args: Iterable[str]) -> List[Tuple[str, List[str]]]:
        """
        Hidden method that returns a list of lists of JSON page data.

        :param args: Various part types that are used to make the requests.
        :return: list: A list of lists of JSON page data.
        """

        results = await self._retrieve_all_part_data(args)
        part_data: List[Tuple[str, List[str]]] = []
        for part, result in results.items():
            html_data = [page["result"]["html"] for page in result]
            part_data.append((part, html_data))
        return part_data
