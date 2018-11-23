import asyncio
import aiohttp
import rapidjson as json


class Scraper:
    _region = "us"
    _base_url = None

    def __init__(self, region: str="us"):
        self._set_region(region)

    def _set_region(self, region: str):
        self._region = region
        self._base_url = self._generate_base_url()

    def _generate_base_url(self) -> str:
        if not self._region == "us":
            return "https://{}.pcpartpicker.com/products/".format(self._region)
        return "https://pcpartpicker.com/products/"

    def _generate_product_url(self, part: str, page_num: int=1) -> str:
        return "{}{}/fetch?page={}".format(self._base_url, part, page_num)

    async def _retrieve_page_numbers(self, session: aiohttp.ClientSession, part: str) -> list:
        data = await self._retrieve_page_data(session, part)
        num = json.loads(data)["result"]["paging_data"]["page_blocks"][-1]["page"]
        return [x for x in range(1, num+1)]

    async def _retrieve_page_data(self, session: aiohttp.ClientSession, part: str, page_num: int=1) -> str:
        page = await session.request('GET', self._generate_product_url(part, page_num))
        return await page.text()

    async def _retrieve_part_data(self, session: aiohttp.ClientSession, part: str):
        page_numbers = await self._retrieve_page_numbers(session, part)
        tasks = [self._retrieve_page_data(session, part, num) for num in page_numbers]
        return await asyncio.gather(*tasks)

    async def _retrieve(self, loop, *args):
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks = [self._retrieve_part_data(session, part) for part in args]
            raw = await asyncio.gather(*tasks)
            return [[json.loads(page)['result']['html'] for page in part_data] for part_data in raw]
