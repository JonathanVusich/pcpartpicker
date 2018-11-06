from .errors import UnsupportedRegion, UnsupportedPart
from .parser import Parser
import asyncio
import aiohttp
import json
from concurrent.futures import ProcessPoolExecutor



class Scraper:
    _supported_types = ["cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                        "video-card", "power-supply", "case", "case-fan", "fan-controller",
                        "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                        "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                        "keyboard", "mouse", "speakers", "ups"]
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

    async def _retrieve_part_data(self, session: aiohttp.ClientSession, part: str):
        if part not in self._supported_types:
            raise UnsupportedPart("Part of type \'{}\' is not supported!".format(part))
        page_numbers = await self._retrieve_page_numbers(session, part)
        tasks = [self._retrieve_page_data(session, part, num) for num in page_numbers]
        return await asyncio.gather(*tasks)

    async def _retrieve_all(self, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = [self._retrieve_part_data(session, part) for part in self._supported_types]
            return await asyncio.gather(*tasks)