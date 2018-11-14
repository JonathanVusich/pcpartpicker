from .parser import Parser
import asyncio
import aiohttp
import json


class Scraper:
    _region = "us"
    _base_url = None
    _parser = None

    def __init__(self, region: str="us"):
        self._set_region(region)
        self._generate_base_url()
        self._parser = Parser()

    def _set_region(self, region: str):
        self._region = region
        self._base_url = self._generate_base_url()

    def _generate_base_url(self) -> str:
        if not self._region == "us":
            return "https://{}.pcpartpicker.com/products/".format(self._region)
        else:
            return "https://pcpartpicker.com/products/"

    def _generate_product_url(self, part: str, page_num: int=1) -> str:
        return "{}{}/fetch?page={}".format(self._base_url, part, page_num)

    async def _retrieve_page_numbers(self, session: aiohttp.ClientSession, part: str) -> list:
        data = await self._retrieve_page_data(session, part, parse=False)
        num = json.loads(data)["result"]["paging_data"]["page_blocks"][-1]["page"]
        return [x for x in range(1, num+1)]

    async def _retrieve_page_data(self, session: aiohttp.ClientSession, part: str, page_num: int=1, parse: bool=True) -> str:
        page = await session.request('GET', self._generate_product_url(part, page_num))
        text = await page.text()
        if parse:
            return await self._parser._parse(part, json.loads(text)['result']['html'])
        return text

    async def _retrieve_part_data(self, session: aiohttp.ClientSession, part: str):
        page_numbers = await self._retrieve_page_numbers(session, part)
        tasks = [self._retrieve_page_data(session, part, num) for num in page_numbers]
        return await asyncio.gather(*tasks)

    async def _retrieve_all(self, loop, supported_parts: list):
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = [self._retrieve_part_data(session, part) for part in supported_parts]
            return await asyncio.gather(*tasks)
