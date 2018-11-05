from .errors import UnsupportedRegion, UnsupportedPart
import asyncio
from itertools import count
import aiohttp
import json
from concurrent.futures import ProcessPoolExecutor



class Scraper:

    _supported_types = ["cpu"]
    _regions = ["au", "be", "ca", "de", "es", "fr",
                    "in", "ie", "it", "nz", "uk", "us"]
    _region = "us"
    _base_url = "https://pcpartpicker.com/products/"

    def __init__(self, region: str="us"):
        self._set_region(region)
        self._generate_base_url()

    @property
    def region(self) -> str:
        return self._region

    def _set_region(self, region: str):
        if not region in self._regions:
            raise UnsupportedRegion("Region \'{}\' is not supported!".format(region))
        self._region = region

    def _generate_base_url(self):
        if not self.region == "us":
            self._base_url = "https://{}.pcpartpicker.com/products/".format(self._region)

    def _generate_product_url(self, part: str, page_num: int=1) -> str:
        return "{}{}/fetch/?page={}".format(self._base_url, part, page_num)

    async def _retrieve_page_data(self, part: str, page_num: int=1) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self._generate_product_url(part, page_num)) as page:
                return await page.text()

    async def _retrieve_url_list(self, part: str):
        num = json.loads(await self._retrieve_page_data(part))["result"]["paging_data"]["page_blocks"][-1]["page"]
        return [self._generate_product_url(part, x) for x in range(1, num+1)]

    async def _dispatch_data(self, url_list: list):
        pool = ProcessPoolExecutor()
        async with  aiohttp.ClientSession() as session:
            coroutines = ()

    async def _retrieve_part_data(self, part: str):
        if part not in self._supported_types:
            raise UnsupportedPart("Part of type \'{}\' is not supported!".format(part))
        result = asyncio.get_event_loop().run_until_complete(self._retrieve_url_list('cpu'))
        data = asyncio.get_event_loop().run_until_complete(self._dispatch_data(result))
