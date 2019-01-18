from itertools import islice
import lxml.html
from moneyed import Money, USD, EUR, GBP, SEK, INR, AUD, CAD, NZD
import re
from typing import List

from .mappings import backlights, clockspeeds, currency_classes, currency_symbols, part_classes, \
    num_pattern, watt_levels
from .parse_utils import Result, retrieve_data, retrieve_int, retrieve_num, to_bytes, audio_bitrate, \
    boolean, case_type, color, default, external_hdd_series, fan_cfm, fan_color, fan_rpm, \
    fan_size, frequency_response, gpu_chipset, gpu_series, grams, hdd_data, hdd_series, interface, \
    kb_backlight, memory_sizes, memory_type, monitor_size, network_speed, rd_speeds, \
    psu_efficiency, psu_modular, psu_series, psu_type, resolution, response_time, sound_card_chipset, \
    wireless_protocols, wr_speeds

from .parts import *


class Parser:
    """Parser:

    This class is designed to parse raw html from PCPartPicker and to transform it into useful data objects.
    """

    _currency_sign = "$"

    _currency = USD

    _region = "us"

    def __init__(self, region: str='us'):
        self._part_funcs = {
                            "cpu": [self._core_clock, self._core_count, self._wattage],
                            "cpu-cooler": [fan_rpm, self._decibels],
                            "motherboard": [default, default, retrieve_int, to_bytes],
                            "memory": [memory_type, default, retrieve_int,
                                       memory_sizes, to_bytes, self._price],
                            "internal-hard-drive": [hdd_series, default, hdd_data,
                                                    to_bytes, self._hdd_cache, self._price],
                            "video-card": [gpu_series, gpu_chipset, to_bytes, self._core_clock],
                            "power-supply": [psu_series, psu_type, psu_efficiency, self._wattage,
                                             psu_modular],
                            "case": [case_type, retrieve_int, retrieve_int, self._wattage],
                            "case-fan": [fan_color, fan_size, fan_rpm, fan_cfm,
                                         self._decibels],
                            "fan-controller": [default, retrieve_int, self._wattage],
                            "thermal-paste": [grams],
                            "optical-drive": [rd_speeds, rd_speeds, rd_speeds, wr_speeds,
                                              wr_speeds, wr_speeds],
                            "sound-card": [sound_card_chipset, retrieve_num, audio_bitrate,
                                           self._snr, self._sample_rate],
                            "wired-network-card": [interface, network_speed],
                            "wireless-network-card": [interface, wireless_protocols],
                            "monitor": [resolution, monitor_size, response_time, self._ips],
                            "external-hard-drive": [external_hdd_series, default,
                                                    to_bytes, self._price],
                            "headphones": [default, boolean, boolean, frequency_response],
                            "keyboard": [default, color, self._kb_switches, kb_backlight],
                            "mouse": [default, default, color],
                            "speakers": [retrieve_num, self._wattage, frequency_response],
                            "ups": [self._wattage, self._va]
                            }

        for func_list in self._part_funcs.values():
            func_list.append(self._price)
        self._optional_funcs = {psu_series, hdd_series}
        self._set_region(region)

    def _set_region(self, region: str):
        """
        Hidden function that changes the currency parsing rules depending on the region.

        :param region: str: The new region to map the rules to.
        :return: None
        """

        self._region = region
        self._currency_sign = currency_symbols[self._region]
        self._currency = currency_classes[self._region]

    def _parse(self, parse_args: tuple) -> tuple:
        """
        Hidden function that parses lists of raw html and returns useful data objects.

        :param parse_args: tuple: The first element of this tuple is the part type that is being parsed,
        the second element is the list of raw html data.
        :return: tuple: The first element of this tuple contains the part type of the parsed data, the
        second element is the list of parsed data objects.
        """

        part, raw_html = parse_args
        part_list = []
        if part in self._part_funcs:
            html = [lxml.html.fromstring(html['html']) for html in raw_html]
            tags = [page.xpath('.//*/text()') for page in html]
            tags = [[tag for tag in page if not tag.startswith(" (")] for page in tags]
            for page in tags:
                for token in retrieve_data(page):
                    part_list.append(self._parse_token(part, token))
        part_list.sort(key=lambda x: x.model)
        return part, part_list

    def _parse_token(self, part: str, data: list):
        """
        Hidden function that parses a list of data depending on the part type.

        :param part: str: The part type of the accompanying data.
        :param data: list: A list of the raw string data for the given part.
        :return: Object: Parsed data object.
        """

        if self._currency_sign in data[0]:
            return
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
                if result.iterate > 1:
                    start_index += result.iterate - 1

        _class = part_classes[part]
        try:
            return _class(*parsed_data)
        except (TypeError, ValueError) as _:
            raise ValueError('Invalid input data for this part!')

    def _price(self, price: str):
        """
        Hidden function that retrieves the price from a raw string.

        :param price: str: Raw string containing currency amount and info.
        :return: Result: Money object extracted from the string.
        """

        if not price:
            return Result(Money("0.00", self._currency))
        elif [x for x in self._currency_sign if x in price]:
            return Result(Money(re.findall(num_pattern, price)[0], self._currency))

    def _core_clock(self, core_clock: str):
        """
        Hidden function that extracts core clock data from a raw string.

        :param core_clock: str: Raw core clock string.
        :return: Result: A ClockSpeed data object generated from the string.
        """

        if not core_clock or self._currency_sign in core_clock \
                or not [speed for speed in clockspeeds.keys() if speed in core_clock]:
            return Result(None, iterate=0)
        for speed_type, func in clockspeeds.items():
            if speed_type in core_clock:
                clock_number = float(re.findall(num_pattern, core_clock)[0])
                return Result(func(clock_number))

    def _core_count(self, core_count: str):
        """
        Hidden function that retrieves core count from a raw string.

        :param core_count: str: Raw core count data.
        :return: Result: Core count
        """

        if not core_count or " W" in core_count or self._currency_sign in core_count:
            return Result(None, iterate=False)
        return retrieve_int(core_count)

    def _decibels(self, decibels: str):
        """
        Hidden function that retrieves decibel data from a raw string.

        :param decibels: Raw decibel data.
        :return: Result: Decibels data object generated from the raw string.
        """

        if not decibels or self._currency_sign in decibels:
            return Result(None, iterate=0)
        num_strings: List[str] = re.findall(num_pattern, decibels)
        nums: List[float] = [float(num) for num in num_strings]
        if "-" in decibels:
            if len(nums) == 2:
                return Result(Decibels(nums[0], nums[1], None))
        return Result(Decibels(None, None, nums[0]))

    def _hdd_cache(self, hdd_cache):
        """
        Hidden function that retrieves byte data from a raw string.

        :param hdd_cache: str: Raw cache size string.
        :return: Result: Size of the HDD cache.
        """

        if not hdd_cache or self._currency_sign in hdd_cache:
            return Result(None, iterate=0)
        return Result(to_bytes(hdd_cache, result=False))

    def _ips(self, ips: str):
        """
        Hidden function that retrieves an IPS value from the given raw string.

        :param ips: str: Raw IPS string.
        :return: Validated IPS string.
        """

        if not ips:
            return Result(None)
        try:
            return boolean(ips)
        except ValueError:
            if self._currency_sign in ips:
                return Result(None, iterate=0)

    def _kb_switches(self, switches: str):
        """
        Hidden function that validates a given keyboard switches string.

        :param switches: str: Raw keyboard switches string.
        :return: Result: Validated interface string.
        """

        if not switches or switches in backlights or self._currency_sign in switches:
            return Result(None, iterate=0)
        return Result(switches)

    def _sample_rate(self, sample_rate: str):
        """
        Hidden function that retrieves the sample rate from a raw string.

        :param sample_rate: str: Raw sample rate data.
        :return: Result: Parsed sample rate data.
        """

        if not sample_rate or self._currency_sign in sample_rate:
            return Result(None)
        return Result(float(re.findall(num_pattern, sample_rate)[0]))

    def _snr(self, snr: str):
        """
        Hidden function that retrieves SNR data from a raw string.

        :param snr: str: Raw SNR data.
        :return: Result: Validated SNR value.
        """

        if not snr or self._currency_sign in snr or " kHz" in snr:
            return Result(None)
        return Result(int(re.findall(num_pattern, snr)[0]))

    def _wattage(self, watt_string: str):
        """
        Hidden function that retrieves watt data from a given string.

        Note: This function coerces all watt values to watts, as there is a fair bit of erroneous
        data on PCPartPicker.

        :param watt_string: str:
        :return: Result: Watt value.
        """

        if not watt_string or self._currency_sign in watt_string or " VA" in watt_string or " kVA" in watt_string:
            return Result(None, iterate=0)
        for watt in watt_levels:
            if watt in watt_string:
                num_string = re.findall(num_pattern, watt_string)[0]
                try:
                    num = int(num_string)
                    if watt == " kW":
                        num *= 1000
                    return Result(num)
                except ValueError:
                    num = float(num_string)
                if watt == " kW":
                    num *= 1000
                    return Result(int(num))
                return Result(num)

    def _va(self, va):
        """
        Hidden function that retrieve volt-ampere data from a raw string.

        :param va: Raw VA data.
        :return: Result: VA data.
        """

        if not va or self._currency_sign in va:
            return Result(None, iterate=0)
        num = float(re.findall(num_pattern, va)[0])
        if " kVA" in va:
            num *= 1000
        return Result(int(num))

