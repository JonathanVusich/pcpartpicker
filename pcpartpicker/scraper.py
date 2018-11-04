from .errors import UnsupportedRegion, UnsupportedPart
import requests
import json

class Scraper:

    _supported_types = ["cpu"]
    _regions = ["au", "be", "ca", "de", "es", "fr",
                    "in", "ie", "it", "nz", "uk", "us"]
    _region = "us"
    _base_url = "https://pcpartpicker.com/products/"

    def __init__(self, region: str="us"):
        self._set_region(region)

    @property
    def region(self) -> str:
        return self._region

    def _set_region(self, region: str):
        if not region in self._regions:
            raise UnsupportedRegion("Region \'{}\' is not supported!".format(region))
        self._region = region

    def _generate_base_url(self):
        if not region == "us":
            self._base_url = "https://{}.pcpartpicker.com/products/".format(self._region)

    def _generate_product_url(self, part: str, page_num: int=1) -> str:
        return "{}{}/#page={}".format(self._base_url, part, page_num)

    def _retrieve_page_num(self, part: str) -> int:
        page = requests.get(self._generate_product_url(part))
        parsed_page = json.loads(page.content.decode('utf-8'))
        return parsed_page["result"]["paging_data"]["page_blocks"][-1]["page"]

    def _yield_part_data(self, part: str):
        if not part in self._supported_types:
            raise UnsupportedPart("Part of type \'{}\' is not supported!".format(part))
        part_num = self._retrieve_page_num(part)
        for x in range(part_num):
            page = requests.get(self._generate_product_url(part, x))
            yield json.loads(page.content.decode('utf-8'))["result"]["html"]
