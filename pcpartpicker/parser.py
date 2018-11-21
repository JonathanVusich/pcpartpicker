import lxml.html
import re
import time
from itertools import islice, chain
from .parts import *

class Parser:

    _float_string = r"(?<![a-zA-Z:])[-+]?\d*\.?\d+"
    _interface_types = ["PCI", "USB"]
    _net_speeds = ["Mbit/s", "Gbit/s"]
    _wireless_protocol_id = ["802.11"]
    _case_types = ["ATX", "ITX", "HTPC"]
    _psu_types = {"ATX", "SFX", "TFX", "EPS", "BTX", "Flex ATX", "Micro ATX", "Mini ITX"}
    _psu_modularity = {"No", "Semi", "Full"}
    _dollar_sign = ["$"]
    _clock_speed = ["GHz", "MHz"]
    _tdp = [" W"]

    def __init__(self):
        self._part_funcs = {"wired-network-card":[self._interface, self._network_speed],
                            "wireless-network-card":[self._interface, self._wireless_protocols],
                            "case":[self._case_type, self._retrieve_int, self._retrieve_int, self._psu_wattage],
                            "power-supply":[self._psu_series, self._psu_type, self._psu_efficiency, self._psu_wattage, self._psu_modular]
                            }
        for func_list in self._part_funcs.values():
            func_list.append(self._price)
        self._part_class_mappings = {"wired-network-card":EthernetCard, "wireless-network-card":WirelessCard,
                                     "case":Case, "power-supply":PSU}

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
        tags = [
            tag
            for tag in tags
            if not tag.startswith(" (")
        ]
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
        func_index = 0
        for x, token in enumerate(islice(data, 1, None)):
            for func in islice(self._part_funcs[part], func_index, None):
                result = await func(token)
                called_funcs.append(func)
                if result:
                    if result.tuple:
                        parsed_data.extend(result.value)
                    else:
                        parsed_data.append(result.value)
                    if result.iterate:
                        break
                    func_index += 1
                    continue
                continue
            func_index += 1

        # Ensure price is set
        uncalled_funcs = [
                         func
                         for func in self._part_funcs[part]
                         if not func in called_funcs
                         ]
        if uncalled_funcs:
            for func in uncalled_funcs:
                result = await func(None)
                if result:
                    if result.tuple:
                        parsed_data.extend(result.value)
                    else:
                        parsed_data.append(result.value)

        _class = self._part_class_mappings[part]
        try:
            return _class(*parsed_data)
        except (TypeError, ValueError) as _:
            print('hi')


    async def _network_speed(self, network_speed: str):
        compatible_speeds = [
            speed
            for speed in self._net_speeds
            if speed in network_speed
        ]
        if compatible_speeds:
            speed = re.findall(self._float_string, network_speed)
            if not speed:
                return Result(None)
            number = int(speed[0])
            if speed[0] == "Mbit/s" and len(speed) == 1:
                return Result((NetworkSpeed.from_Mbits(number), 1), tuple=True)
            elif speed[0] == "Mbit/s" and len(speed) == 2:
                return Result((NetworkSpeed.from_Mbits(number), int(speed[1])), tuple=True)
            elif len(speed) == 1:
                return Result((NetworkSpeed.from_Gbits(number), 1), tuple=True)
            return Result(NetworkSpeed.from_Gbits(number), int(speed[1]), tuple=True)
        return Result(None, iterate=False)

    async def _interface(self, interface: str):
        for inter in self._interface_types:
            if inter in interface:
                return Result(interface)

    async def _wireless_protocols(self, protocols: str):
        if [x for x in self._wireless_protocol_id if x in protocols]:
            return Result(protocols)

    async def _case_type(self, case_type: str):
        for case in self._case_types:
            if case in case_type:
                return Result(case_type)

    async def _retrieve_int(self, string: str):
        try:
            return Result(int(string))
        except ValueError:
            return None

    async def _psu_wattage(self, psu_string: str):
        if " W" in psu_string and len([x for x in psu_string if x.isnumeric()]) > 2:
            return Result(int(re.findall(self._float_string, psu_string)[0]))

    async def _psu_type(self, psu_type: str):
        if psu_type in self._psu_types:
            return Result(psu_type)

    async def _psu_modular(self, psu_modularity: str):
        if psu_modularity in self._psu_modularity:
            return Result(psu_modularity)

    async def _psu_series(self, series: str):
        psu_type = await self._psu_type(series)
        if psu_type:
            return Result(None, iterate=False)
        return Result(series)

    async def _psu_efficiency(self, efficiency: str):
        if efficiency == "-":
            return Result(None)
        return Result(efficiency)

    async def _price(self, price: str):
        if not price:
            return Result(Decimal("0.00"))
        elif [x for x in self._dollar_sign if x in price]:
            return Result(Decimal(re.findall(self._float_string, price)[0]))


class Result:

    def __init__(self, value, iterate=True, tuple=False):
        self.value = value
        self.iterate = iterate
        self.tuple = tuple

    def __repr__(self):
        return f"Value: {self.value}, Iterate: {self.iterate}, Tuple: {self.tuple}"
