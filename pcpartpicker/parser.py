import lxml.html, lxml.etree
import re
import time
from itertools import islice
from .parts import *
import rapidjson as json
from moneyed import Money, USD, EUR, GBP, SEK, INR, AUD, CAD, NZD

class Parser:

    _float_string = r"(?<![a-zA-Z:])[-+]?\d*\.?\d+"
    _interface_types = ["PCI", "USB"]
    _net_speeds = ["Mbit/s", "Gbit/s"]
    _byte_size_types = {"GB":Bytes.from_GB, "TB":Bytes.from_TB, "MB":Bytes.from_MB,
                        "KB":Bytes.from_KB, "PB":Bytes.from_PB}
    _wireless_protocol_id = ["802.11"]
    _case_types = ["ATX", "ITX", "HTPC"]
    _psu_types = {"ATX", "SFX", "TFX", "EPS", "BTX", "Flex ATX", "Micro ATX", "Mini ITX"}
    _psu_modularity = {"No", "Semi", "Full"}
    _chipset_types = ["GeForce ", "Radeon ", "Vega ", "Titan ", "Quadro ", "NVS ", "FirePro ", "FireGL "]
    _currency_symbol_mappings = {"us" : "$", "au" : "$", "ca" : "$", "be" : "€", "de" : "€", "es" : "€", "fr" : "€",
                                 "ie" : "€", "it" : "€", "nl" : "€", "nz" : "$", "se" : "kr", "uk" : "£", "in" : "₹"}
    _currency_class_mappings = {"us" : USD, "au" : AUD, "ca" : CAD, "be" : EUR, "de" : EUR, "es" : EUR, "fr" : EUR,
                                "ie" : EUR, "it" : EUR, "nl" : EUR, "nz" : NZD, "se" : SEK, "uk" : GBP, "in": INR}
    _currency_sign = "$"
    _clock_speed = {"GHz":ClockSpeed.from_GHz, "MHz":ClockSpeed.from_MHz}
    _tdp = [" W"]
    _region = "us"

    def __init__(self):
        self._part_funcs = {"wired-network-card":[self._interface, self._network_speed],
                            "wireless-network-card":[self._interface, self._wireless_protocols],
                            "case":[self._case_type, self._retrieve_int, self._retrieve_int, self._psu_wattage],
                            "power-supply":[self._psu_series, self._psu_type, self._psu_efficiency, self._psu_wattage,
                                            self._psu_modular],
                            "video-card":[self._gpu_series, self._gpu_chipset, self._bytes, self._core_clock]
                            }
        for func_list in self._part_funcs.values():
            func_list.append(self._price)
        self._part_class_mappings = {"wired-network-card":EthernetCard, "wireless-network-card":WirelessCard,
                                     "case":Case, "power-supply":PSU, "video-card":GPU}

        self._optional_funcs = {self._psu_series}

    def _update_region(self, region: str):
        self._region = region
        self._currency_sign = self._currency_symbol_mappings[self._region]

    def _parse(self, part: str, raw_html: str):
        part_list = []
        if part in self._part_funcs:
            html = json.loads(raw_html)['result']['html']
            html = lxml.html.fromstring(html)
            tags = html.xpath('.//*/text()')
            tags = [
                    tag
                    for tag in tags
                    if not tag.startswith(" (")
                    ]
            for token in Parser._retrieve_data(tags):
                part_list.append(self._parse_token(part, token))
        return part_list

    @staticmethod
    def _retrieve_data(tags: list):
        start_index = 0
        while start_index < len(tags):
            it = None
            for y, tag in enumerate(islice(tags, start_index, None)):
                if tag == "Add":
                    it = tags[start_index:start_index + y]
                    start_index += y+1
                    break
            if not it:
                return
            yield it

    def _parse_token(self, part: str, data: list):
        parsed_data = [data[0]]
        start_index = 1
        for x, func in enumerate(self._part_funcs[part]):
            if func in self._optional_funcs:
                result = func(list(islice(data, start_index+x, start_index+x+2)))
            else:
                try:
                    result = func(data[start_index+x])
                except IndexError:
                    result = func(None)
            if result:
                if result.tuple:
                    parsed_data.extend(result.value)
                else:
                    parsed_data.append(result.value)
                if not result.iterate:
                    start_index -= 1

        _class = self._part_class_mappings[part]
        try:
            return _class(*parsed_data)
        except (TypeError, ValueError) as _:
            print('hi')

    def _bytes(self, byte_string: str):
        for byte_type, func in self._byte_size_types.items():
            if byte_type in byte_string:
                byte_num = float(re.findall(self._float_string, byte_string)[0])
                return Result(func(byte_num))

    def _core_clock(self, core_clock: str):
        if not core_clock or self._currency_sign in core_clock:
            return Result(None, iterate=False)
        for speed_type, func in self._clock_speed.items():
            if speed_type in core_clock:
                clock_number = float(re.findall(self._float_string, core_clock)[0])
                return Result(func(clock_number))

    def _network_speed(self, network_speed: str):
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
            if "Mbit/s" in compatible_speeds and len(speed) == 1:
                return Result((NetworkSpeed.from_Mbits(number), 1), tuple=True)
            elif "Mbit/s" in compatible_speeds and len(speed) == 2:
                return Result((NetworkSpeed.from_Mbits(number), int(speed[1])), tuple=True)
            elif len(speed) == 1:
                return Result((NetworkSpeed.from_Gbits(number), 1), tuple=True)
            return Result((NetworkSpeed.from_Gbits(number), int(speed[1])), tuple=True)
        return Result(None, iterate=False)

    def _interface(self, interface: str):
        for inter in self._interface_types:
            if inter in interface:
                return Result(interface)

    def _wireless_protocols(self, protocols: str):
        if [x for x in self._wireless_protocol_id if x in protocols]:
            return Result(protocols)

    def _case_type(self, case_type: str):
        for case in self._case_types:
            if case in case_type:
                return Result(case_type)

    def _retrieve_int(self, string: str):
        try:
            return Result(int(string))
        except ValueError:
            return None

    def _psu_wattage(self, psu_string: str):
        if not psu_string or self._currency_sign in psu_string:
            return Result(None, iterate=False)
        elif " W" in psu_string:
            return Result(int(re.findall(self._float_string, psu_string)[0]))

    def _psu_type(self, psu_type: str):
        if psu_type in self._psu_types:
            return Result(psu_type)

    def _psu_modular(self, psu_modularity: str):
        if psu_modularity in self._psu_modularity:
            return Result(psu_modularity)

    def _gpu_series(self, series: str):
        chipset_matches = [chipset for chipset in self._chipset_types if chipset in series]
        if not chipset_matches:
            return Result(series)
        return Result(None, iterate=False)

    def _gpu_chipset(self, chipset: str):
        for c in self._chipset_types:
            if c in chipset:
                return Result(chipset)

    def _psu_series(self, series: list):
        psu_type = self._psu_type(series[0])
        if psu_type:
            if self._psu_type(series[1]):
                return Result(series[0])
            return Result(None, iterate=False)
        return Result(series[0])

    def _psu_efficiency(self, efficiency: str):
        if efficiency == "-":
            return Result(None)
        elif "80+" in efficiency:
            return Result(efficiency)

    def _price(self, price: str):
        if not price:
            return Result(Money("0.00", self._currency_class_mappings[self._region]))
        elif [x for x in self._currency_sign if x in price]:
            return Result(Money(re.findall(self._float_string, price)[0], self._currency_class_mappings[self._region]))


class Result:

    def __init__(self, value, iterate=True, tuple=False):
        self.value = value
        self.iterate = iterate
        self.tuple = tuple

    def __repr__(self):
        return f"Value: {self.value}, Iterate: {self.iterate}, Tuple: {self.tuple}"
