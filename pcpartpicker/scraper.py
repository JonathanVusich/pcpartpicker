import asyncio
import logging
from typing import Iterable, Dict

import aiohttp

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class Scraper:
    """Scraper:

    This class is designed to retrieve http requests in a fast and efficient manner.

    Attributes:
        region: str:
            This variable holds the region that is used to build URLs for PCPartPicker.
        base_url: str:
            This variable holds the product URL from which the actual request URLs are built.

    """

    def __init__(self, region: str = "us") -> None:
        self.region: str = region
        self.base_url: str = "https://jonathanvusich.github.io/pcpartpicker-scraper/"

    def generate_product_url(self, part: str) -> str:
        return f"{self.base_url}{self.region}/{part}"

    async def retrieve(self, args: Iterable[str]) -> Dict[str, str]:
        parts = [arg for arg in args]
        urls = [self.generate_product_url(part) for part in parts]
        async with aiohttp.ClientSession() as session:
            requests = [session.get(url) for url in urls]
            results = await asyncio.gather(*requests, return_exceptions=True)
            retry_parts = []
            final_results = {}
            for part, result in zip(parts, results):
                if isinstance(result, asyncio.TimeoutError):
                    logger.debug(f"Fetching data for {part} timed out! Retrying...")
                    retry_parts.append(part)
                elif isinstance(result, Exception):
                    raise result
                else:
                    final_results.update({part: await result.text()})

        if retry_parts:
            final_results.update(await self.retrieve(retry_parts))
        return final_results
