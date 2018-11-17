import lxml.html
import re
import time
from itertools import islice
from .parts import *

class Parser:

    _float_string = r"(?<![a-zA-Z:])[-+]?\d*\.?\d+"
    _interface_types = ["PCI", "USB"]
    _net_speeds = ["Mbit/s", "Gbit/s"]
    _dollar_sign = "$"
    _clock_speed = ["GHz", "MHz"]
    _tdp = [" W"]

    def __init__(self):
        self._part_funcs = {"wired-network-card":[self._interface, self._network_speed, self._price]}
        self._part_class_mappings = {"wired-network-card":EthernetCard}

    async def _parse(self, part: str, raw_html: str):
        part_list = []
        if part in self._part_funcs:
            start = time.perf_counter()
            html = lxml.html.fromstring(raw_html)
            tags = html.xpath('.//*/text()')
            async for token in Parser._retrieve_data(tags):
                part_list.append(await self._parse_token(part, token))
            print(time.perf_counter() - start)
        return part_list

    @staticmethod
    async def _retrieve_data(tags: list):
        tags = [tag for tag in tags if not tag.startswith(" (")]
        start_index = 0
        it = None
        while start_index < len(tags):
            for y, tag in enumerate(islice(tags, start_index, None)):
                if tag == "Add":
                    it = tags[start_index:start_index + y]
                    start_index += y+1
                    break
            yield it

    async def _parse_token(self, part: str, data: list):
        parsed_data = [data[0]]
        for x, token in enumerate(islice(data, 1, None)):
            for func in islice(self._part_funcs[part], x, None):
                result = await func(token)
                if isinstance(result, tuple):
                    parsed_data.extend(result)
                else:
                    parsed_data.append(result)
                if result:
                    break
        _class = self._part_class_mappings[part]
        return _class(*parsed_data)

    async def _network_speed(self, network_speed: str):
        for speed in self._net_speeds:
            if speed in network_speed:
                nums = re.findall(self._float_string, network_speed)
                if not nums:
                    return None, None
                else:
                    bits = int(nums[0])
                    if speed == "Mbit/s":
                        speed = NetworkSpeed.from_Mbits(bits)
                    else:
                        speed = NetworkSpeed.from_Gbits(bits)
                    if len(nums) == 2:
                        return speed, int(nums[1])
                    else:
                        return speed, 1

    async def _interface(self, interface: str):
        for inter in self._interface_types:
            if inter in interface:
                return interface

    async def _price(self, price: str):
        if self._dollar_sign in price:
            return Decimal(re.findall(self._float_string, price)[0])

