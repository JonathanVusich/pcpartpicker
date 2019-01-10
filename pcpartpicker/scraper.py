import asyncio
import aiohttp


class Scraper:
    """Scraper:

    This class is designed to retrieve http requests in a fast and efficient manner.

    Attributes:
        _region: str:
            This variable holds the region that is used to build URLs for PCPartPicker.
        _base_url: str:
            This variable holds the product URL from which the actual request URLs are built.

    """

    _region = "us"
    _base_url = None

    def __init__(self, region: str="us"):
        self._set_region(region)

    def _set_region(self, region: str):
        """
        Hidden method that is used to handle region changes.

        :param region: str: Represents the new region that the scraper will pull data from.
        :return: None
        """

        self._region = region
        self._base_url = self._generate_base_url()

    def _generate_base_url(self) -> str:
        """
        Hidden method that is used to generate the base URL for regional requests.

        :return: str: Represents the base URL for regional requests.
        """

        if not self._region == "us":
            return "https://{}.pcpartpicker.com/products/".format(self._region)
        return "https://pcpartpicker.com/products/"

    def _generate_product_url(self, part: str, page_num: int=1) -> str:
        """
        Hidden method that is used to generate specific URLs for products.
        Relies on the base URL for generation.

        :param part: str: Represents the part data to retrieve.
        :param page_num: Represents the page number to retrieve.
        :return: str: The URL that represents the specific page for the given part.
        """

        return "{}{}/fetch?page={}".format(self._base_url, part, page_num)

    async def _retrieve_page_numbers(self, session: aiohttp.ClientSession, part: str) -> list:
        """
        Hidden method that retrieves a list of page numbers for a given part type.

        :param session: aiohttp.ClientSession: The asynchronous session used for making requests.
        :param part: str: The part type.
        :return: list: A list of numbers that represents the different page numbers of the given part type.
        """

        data = await self._retrieve_page_data(session, part)
        num = data["paging_data"]["page_blocks"][-1]["page"]
        return [x for x in range(1, num+1)]

    async def _retrieve_page_data(self, session: aiohttp.ClientSession, part: str, page_num: int=1) -> str:
        """
        Hidden method that retrieves page data for a given part type and page number.

        :param session: aiohttp.ClientSession: The asynchronous session used for making requests.
        :param part: str: The part type.
        :param page_num: int: The page number.
        :return: str: The raw page data for this request.
        """

        while True:
            page = await session.request('GET', self._generate_product_url(part, page_num))
            if page.status == 200:
                break
        data = await page.json(content_type=None)
        return data["result"]

    async def _retrieve_part_data(self, session: aiohttp.ClientSession, part: str) -> list:
        """
        Hidden method that returns a list of raw page data for a given part.

        :param session: aiohttp.ClientSession: The asynchronous session that is used to generate requests.
        :param part: str: The part type to retrieve.
        :return: list: A list of raw page data for the given part.
        """

        page_numbers = await self._retrieve_page_numbers(session, part)
        tasks = [self._retrieve_page_data(session, part, num) for num in page_numbers]
        return await asyncio.gather(*tasks)

    async def _retrieve(self, loop, *args):
        """
        Hidden method that returns a list of lists of JSON page data.

        :param loop: The event loop that is used to make asynchronous requests.
        :param args: Various part types that are used to make the requests.
        :return: list: A list of lists of JSON page data.
        """

        connector = aiohttp.TCPConnector(limit=75, ttl_dns_cache=300)
        async with aiohttp.ClientSession(loop=loop, connector=connector) as session:
            tasks = [self._retrieve_part_data(session, part) for part in args]
            return await asyncio.gather(*tasks)

