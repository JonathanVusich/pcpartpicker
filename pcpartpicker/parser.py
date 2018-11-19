import lxml.html
import re
import time
from itertools import islice
from .parts import *

class Parser:

    _float_string = r"(?<![a-zA-Z:])[-+]?\d*\.?\d+"
    _interface_types = ["PCI", "USB"]
    _net_speeds = ["Mbit/s", "Gbit/s"]
    _wireless_protocol_id = "802.11"
    _case_types = ["ATX", "ITX", "HTPC"]
    _dollar_sign = "$"
    _clock_speed = ["GHz", "MHz"]
    _tdp = [" W"]

    def __init__(self):
        self._part_funcs = {"wired-network-card":[self._interface, self._network_speed, self._price],
                            "wireless-network-card":[self._interface, self._wireless_protocols, self._price],
                            "case":[self._case_type, self._retrieve_int, self._retrieve_int, self._case_psu, self._price],
                            }
        self._part_class_mappings = {"wired-network-card":EthernetCard, "wireless-network-card":WirelessCard,
                                     "case":Case}

    async def _parse(self, part: str, raw_html: str):
        part_list = []
        if part in self._part_funcs:
            start = time.perf_counter()
            html = lxml.html.fromstring(raw_html)
            tags = html.xpath('.//*/text()')
            async for token in Parser._retrieve_data(tags):
                part_list.append(await self._parse_token(part, token))
            print(time.perf_counter() - start)
            print('hi')
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
        called_funcs = []
        x = 0
        for token in islice(data, 1, None):
            for func in islice(self._part_funcs[part], x, None):
                result = await func(token)
                called_funcs.append(func)
                if result:
                    result, proceed = result
                    if isinstance(result, tuple):
                        parsed_data.extend(result)
                    else:
                        parsed_data.append(result)
                    if proceed:
                        break
                else:
                    continue
            x = x + 1
        # Ensure price is set
        uncalled_funcs = [func for func in self._part_funcs[part] if not func in called_funcs]
        if uncalled_funcs:
            for func in uncalled_funcs:
                parsed_data.append(await func(" "))
        _class = self._part_class_mappings[part]
        try:
            return _class(*parsed_data)
        except (TypeError, ValueError) as _:
            print('hi')


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
                        return (speed, int(nums[1])), True
                    else:
                        return (speed, 1), True

    async def _interface(self, interface: str):
        for inter in self._interface_types:
            if inter in interface:
                return interface, True

    async def _wireless_protocols(self, protocols: str):
        if self._wireless_protocol_id in protocols:
            return protocols, True

    async def _case_type(self, case_type: str):
        for case in self._case_types:
            if case in case_type:
                return case_type, True

    async def _retrieve_int(self, string: str):
        try:
            return int(string), True
        except ValueError:
            return None

    async def _case_psu(self, psu_string: str):
        if "W" in psu_string:
            return int(re.findall(self._float_string, psu_string)[0]), True
        elif psu_string == " ":
            return None
        return None, False

    async def _price(self, price: str):
        if self._dollar_sign in price:
            return Decimal(re.findall(self._float_string, price)[0]), True
        elif price == " ":
            return Decimal("0.00")
