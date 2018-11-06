from .errors import UnsupportedRegion, UnsupportedPart
from .parser import Parser
import asyncio
import aiohttp
import json
from concurrent.futures import ProcessPoolExecutor



class Scraper:

    _supported_types = ["cpu"]
    _regions = ["au", "be", "ca", "de", "es", "fr",
                    "in", "ie", "it", "nz", "uk", "us"]
    _region = "us"
    _base_url = "https://pcpartpicker.com/products/"
    _parser = None

    def __init__(self, region: str="us"):
        self._set_region(region)
        self._generate_base_url()
        self._parser = Parser()

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

    async def _retrieve_page_numbers(self, session: aiohttp.ClientSession, part: str):
        num = json.loads(await self._retrieve_page_data(session, part))["result"]["paging_data"]["page_blocks"][-1]["page"]
        return [x for x in range(1, num+1)]

    async def _retrieve_page_data(self, session: aiohttp.ClientSession, part: str, page_num: int=1) -> str:
        page = await session.request('GET', self._generate_product_url(part, page_num))
        return await page.text()

    async def _process_page(self, part: str, raw_html: str):
        await self._parser._parse(raw_html)

    async def _retrieve_parsed_parts(self, pool: ProcessPoolExecutor, session: aiohttp.ClientSession, part: str, page_num: int) -> dict:
        raw_html = self._retrieve_page_data(session, part, page_num)
        return await asyncio.wrap_future(pool.submit(self._process_page, part, raw_html))

    async def _fetch_data(self, session: aiohttp.ClientSession, part: str, page_numbers: list):
        pool = ProcessPoolExecutor()
        coroutines = (self._retrieve_parsed_parts(pool, session, part, num) for num in page_numbers)
        return await asyncio.gather(*coroutines)

    async def _retrieve_part_data(self, pool: ProcessPoolExecutor, part: str):
        if part not in self._supported_types:
            raise UnsupportedPart("Part of type \'{}\' is not supported!".format(part))
        async with aiohttp.ClientSession() as session:
            page_numbers = await self._retrieve_page_numbers(session, part)
            await asyncio.wrap_future(pool.submit(setattr(self, part, await self._fetch_data(session, part, page_numbers))))

    def _retrieve_all(self):
        pool = ProcessPoolExecutor()
        coroutines = (self._retrieve_part_data(pool, part) for part in self._supported_types)
        asyncio.run_coroutine_threadsafe(*coroutines)