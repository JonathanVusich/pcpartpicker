import lxml.html
import re
from itertools import islice
from .parts import *
from moneyed import Money, USD, EUR, GBP, SEK, INR, AUD, CAD, NZD


class Parser:
    """Parser:

    This class is designed to parse raw html from PCPartPicker and to transform it into useful data objects.
    """

    _float_string = r"(?<![a-zA-Z:])[-+]?\d*\.?\d+"

    _part_class_mappings = {
        "cpu": CPU,
        "cpu-cooler": CPUCooler,
        "motherboard": Motherboard,
        "memory": Memory,
        "wired-network-card": EthernetCard,
        "wireless-network-card": WirelessCard,
        "case": Case,
        "power-supply": PSU,
        "video-card": GPU,
        "internal-hard-drive": StorageDrive,
        "case-fan": Fan,
        "fan-controller": FanController,
        "thermal-paste": ThermalPaste,
        "optical-drive": OpticalDrive,
        "sound-card": SoundCard,
        "monitor": Monitor,
        "external-hard-drive": ExternalHDD,
        "headphones": Headphones,
        "keyboard": Keyboard,
        "mouse": Mouse,
        "speakers": Speakers,
        "ups": UPS
    }

    _hdd_form_factors = {"1.8\"", "2.5\"", "3.5\"", "M.2-22110", "M.2-2242",
                         "M.2-2260", "M.2-2280", "mSATA", "PCI-E"}

    _colors = {"Black", "Beige", "Beige / Gray", "Beige / Black", "Black / Beige", "Black / Blue", "Black / Gold",
               "Black / Gray", "Black / Green", "Black / Multicolor", "Black / Orange", "Black / Pink",
               "Black / Purple", "Black / Red", "Black / Silver", "Black / White", "Black / Yellow", "Blue",
               "Blue / Black", "Blue / Gray", "Blue / Pink", "Blue / Silver", "Blue / White", "Brown",
               "Brown / Black", "Camo", "Gold", "Dark Silver", "Gold / White", "Gray", "Gray / Black", "Gray / Blue",
               "Gray / Silver", "Gray / White", "Gray / White", "Gray / Yellow", "Green", "Green / Black",
               "Green / Blue", "Green / Silver", "Green / White", "Gunmetal", "Multicolor", "Orange",
               "Orange / Black", "Orange / White", "Pink", "Pink / Black", "Pink / White", "Purple", "Purple / Black",
               "Red", "Red / White", "Red / Black", "Red / Blue", "Red / Silver", "Silver", "Silver / Black",
               "Silver / Beige", "Silver / Black", "Silver / Blue", "Silver / Gray", "Silver / White",
               "White", "White / Black", "White / Blue", "White / Gray", "White / Purple", "White / Red",
               "White / Pink", "White / Silver", "White / Yellow", "Yellow / Black", "Yellow"}

    _backlight_types = {"No", "Yellow", "White", "Red/Blue", "Red/Amber", "Red", "Purple",
                        "Orange", "Multicolor", "Green", "Blue/Silver", "Blue"}

    _interface_types = ["PCI", "USB"]

    _net_speeds = ["Mbit/s", "Gbit/s"]

    _byte_size_types = {"GB":Bytes.from_GB, "TB":Bytes.from_TB, "MB":Bytes.from_MB,
                        "KB":Bytes.from_KB, "PB":Bytes.from_PB}

    _wireless_protocol_id = ["802.11"]

    _case_types = {"ATX Desktop", "ATX Full Tower", "ATX Mid Tower", "ATX Mini Tower", "ATX Test Bench", "HTPC",
                   "MicroATX Desktop", "MicroATX Mid Tower", "MicroATX Mini Tower", "MicroATX Slim",
                   "Mini ITX Desktop", "Mini ITX Test Bench", "Mini ITX Tower"}

    _audio_bitrates = {"24", "16"}

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

    _watt_ratings = [" W", " kW", " mW", " nW"]

    _region = "us"

    def __init__(self, region: str='us'):
        self._part_funcs = {
                            "cpu":[self._core_clock, self._core_count, self._wattage],
                            "cpu-cooler":[self._fan_rpm, self._decibels],
                            "motherboard":[self._default, self._default, self._retrieve_int, self._bytes],
                            "memory": [self._memory_type, self._default, self._retrieve_int,
                                       self._memory_sizes, self._bytes, self._price],
                            "internal-hard-drive": [self._hdd_series, self._default, self._hdd_data,
                                                    self._bytes, self._hdd_cache, self._price],
                            "video-card": [self._gpu_series, self._gpu_chipset, self._bytes, self._core_clock],
                            "power-supply": [self._psu_series, self._psu_type, self._psu_efficiency, self._wattage,
                                             self._psu_modular],
                            "case": [self._case_type, self._retrieve_int, self._retrieve_int, self._wattage],
                            "case-fan": [self._fan_color, self._fan_size, self._fan_rpm, self._fan_cfm,
                                        self._decibels],
                            "fan-controller": [self._default, self._retrieve_int, self._wattage],
                            "thermal-paste": [self._grams],
                            "optical-drive": [self._rd_speeds, self._rd_speeds, self._rd_speeds, self._wr_speeds,
                                              self._wr_speeds, self._wr_speeds],
                            "sound-card": [self._sound_card_chipset, self._retrieve_num, self._audio_bitrate,
                                           self._snr, self._sample_rate],
                            "wired-network-card": [self._interface, self._network_speed],
                            "wireless-network-card": [self._interface, self._wireless_protocols],
                            "monitor": [self._resolution, self._monitor_size, self._response_time, self._ips],
                            "external-hard-drive": [self._external_hdd_series, self._default,
                                                    self._bytes, self._price],
                            "headphones": [self._default, self._boolean, self._boolean, self._frequency_response],
                            "keyboard": [self._default, self._color, self._kb_switches, self._kb_backlight],
                            "mouse": [self._default, self._default, self._color],
                            "speakers": [self._retrieve_num, self._wattage, self._frequency_response],
                            "ups": [self._wattage, self._va]
                            }

        for func_list in self._part_funcs.values():
            func_list.append(self._price)
        self._optional_funcs = {self._psu_series, self._hdd_series}
        self._set_region(region)

    def _set_region(self, region: str):
        """
        Hidden function that changes the currency parsing rules depending on the region.

        :param region: str: The new region to map the rules to.
        :return: None
        """

        self._region = region
        self._currency_sign = self._currency_symbol_mappings[self._region]

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
            html = [lxml.html.fromstring(html) for html in raw_html]
            tags = [page.xpath('.//*/text()') for page in html]
            tags = [[tag for tag in page if not tag.startswith(" (")] for page in tags]
            for page in tags:
                for token in self._retrieve_data(page):
                    part_list.append(self._parse_token(part, token))
        return part, part_list

    def _retrieve_data(self, tags: list):
        """
        Hidden generator that yields up chunks of part data.

        :param tags: list: The raw tags returned from the lxml parser.
        :return: List of individual part data.
        """

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

        _class = self._part_class_mappings[part]
        try:
            return _class(*parsed_data)
        except (TypeError, ValueError) as _:
            raise ValueError('Invalid input data for this part!')

    def _retrieve_int(self, string: str):
        """
        Hidden function that parses strings to integers.

        :param string: str: The raw int string.
        :return: Result: The value retrieved from the string.
        """
        if not string:
            return Result(None, iterate=0)
        try:
            return Result(int(string))
        except ValueError:
            if "N/A" in string or "-" in string:
                return Result(None)
            raise ValueError("Not a valid int string!")

    def _retrieve_float(self, string: str):
        """
        Hidden function that parses strings to floats.

        :param string: str: The raw float string.
        :return: Result: The value returned from the string.
        """

        try:
            return Result(float(string))
        except ValueError:
            if "N/A" in string or "-" in string:
                return Result(None)
            raise ValueError("Not a valid float string!")

    def _retrieve_num(self, string: str):
        """
        Hidden function that attempts to retrieve a numeric value from a string.

        :param string: str: The raw numeric string.
        :return: Result: The numeric value retrieved from the string.
        """

        try:
            return self._retrieve_int(string)
        except ValueError:
            try:
                return self._retrieve_float(string)
            except ValueError:
                raise ValueError("Not a valid numeric string!")

    def _bytes(self, byte_string: str, result=True):
        """
        Hidden function that parses a string representing binary size to a Bytes data object.

        :param byte_string: str: The raw string representing binary size.
        :param result: Determines whether or not the return type of this function should be a
        Result object or the Bytes object.
        :return: Result, Bytes:
        """

        if not byte_string:
            return Result(None)
        for byte_type, func in self._byte_size_types.items():
            if byte_type in byte_string:
                byte_num = float(re.findall(self._float_string, byte_string)[0])
                if result:
                    return Result(func(byte_num))
                return func(byte_num)

    def _boolean(self, boolean: str):
        """
        Hidden function that returns a boolean value from a string.

        :param boolean: str: The raw boolean string.
        :return: Result: The boolean value extracted from the string.
        """

        if boolean == "Yes":
            return Result(True)
        elif boolean == "No":
            return Result(False)
        raise ValueError("Not a valid boolean!")

    def _price(self, price: str):
        """
        Hidden function that retrieves the price from a raw string.

        :param price: str: Raw string containing currency amount and info.
        :return: Result: Money object extracted from the string.
        """

        if not price:
            return Result(Money("0.00", self._currency_class_mappings[self._region]))
        elif [x for x in self._currency_sign if x in price]:
            return Result(Money(re.findall(self._float_string, price)[0], self._currency_class_mappings[self._region]))

    def _audio_bitrate(self, audio_br: str):
        """
        Hidden function that extract audio bitrate data from a string.

        :param audio_br: str: The raw audio bitrate string.
        :return: Result: The audio bitrate extracted from the string
        """
        if audio_br == "None":
            return Result(None)
        if audio_br in self._audio_bitrates:
            return Result(int(audio_br))

    def _case_type(self, case_type: str):
        """
        Hidden function that returns the case type string if it is of a valid type.

        :param case_type: str: The raw case type string.
        :return: Result: The verified case type.
        """

        if case_type in self._case_types:
            return Result(case_type)

    def _color(self, color: str):
        """
        Hidden function that returns the given string if is a valid color.

        :param color: str: The raw color string.
        :return: Result: The verified color string.
        """
        if not color or color not in self._colors:
            return Result(None, iterate=0)
        return Result(color)

    def _core_clock(self, core_clock: str):
        """
        Hidden function that extracts core clock data from a raw string.

        :param core_clock: str: Raw core clock string.
        :return: Result: A ClockSpeed data object generated from the string.
        """

        if not core_clock or self._currency_sign in core_clock \
                or not [speed for speed in self._clock_speed.keys() if speed in core_clock]:
            return Result(None, iterate=0)
        for speed_type, func in self._clock_speed.items():
            if speed_type in core_clock:
                clock_number = float(re.findall(self._float_string, core_clock)[0])
                return Result(func(clock_number))

    def _core_count(self, core_count: str):
        """
        Hidden function that retrieves core count from a raw string.

        :param core_count: str: Raw core count data.
        :return: Result: Core count
        """

        if not core_count or " W" in core_count or self._currency_sign in core_count:
            return Result(None, iterate=False)
        return self._retrieve_int(core_count)

    def _decibels(self, decibels: str):
        """
        Hidden function that retrieves decibel data from a raw string.

        :param decibels: Raw decibel data.
        :return: Result: Decibels data object generated from the raw string.
        """

        if not decibels or self._currency_sign in decibels:
            return Result(None, iterate=0)
        nums = re.findall(self._float_string, decibels)
        nums = [float(num) for num in nums]
        if "-" in decibels:
            if len(nums) == 2:
                return Result(Decibels(nums[0], nums[1], None))
        return Result(Decibels(None, None, nums[0]))

    def _default(self, default_str: str):
        """
        Placeholder function that simply returns the string as is.

        :param default_str: str: The default string
        :return: Result: The default string.
        """

        return Result(default_str)

    def _external_hdd_series(self, series: str):
        """
        Hidden function that verifies that the given string is a compatible external HDD type.

        :param series: str: Raw HDD type.
        :return: Result: The verified HDD type.
        """

        if series == "Desktop" or series == "Portable":
            return Result(None, iterate=0)
        return Result(series)

    def _fan_cfm(self, fan_cfm: str):
        """
        Hidden function that generates fan airflow data from a raw string.

        :param fan_cfm: str: The raw airflow data.
        :return: Result: Data object representing airflow data.
        """

        if fan_cfm == "N/A":
            return Result(None)
        nums = [float(num) for num in re.findall(self._float_string, fan_cfm)]
        if len(nums) == 2:
            return Result(CFM(nums[0], nums[1], None))
        if len(nums) == 1:
            return Result(CFM(None, None, nums[0]))

    def _fan_color(self, fan_color: str):
        """
        Hidden function that checks fan color validity.

        :param fan_color: str: Raw color string.
        :return: Result: Validated color string.
        """

        if self._fan_size(fan_color):
            return Result(None, iterate=0)
        return Result(fan_color)

    def _fan_rpm(self, rpm: str):
        """
        Hidden function that returns fan rpm data from a raw string.

        :param rpm: str: Raw fan data.
        :return: Result: Data object representing fan RPM.
        """

        if not rpm or rpm == "N/A" or rpm == "-":
            return Result(None)
        nums = re.findall(self._float_string, rpm)
        nums = [int(num) for num in nums]
        if "-" in rpm:
            if len(nums) == 2:
                return Result(RPM(nums[0], nums[1], None))
            raise ValueError("Not a valid number of numeric values!")
        if len(nums) == 1:
            return Result(RPM(None, None, nums[0]))
        raise ValueError("Not a valid number of numeric values!")

    def _fan_size(self, fan_size: str):
        """
        Hidden function that retrieves fan size in integers from a raw string.

        :param fan_size: str: Raw fan size data.
        :return: Result: Fan size in mm.
        """

        if "mm" in fan_size and len([x for x in fan_size if x.isnumeric()]) > 1:
            return Result(int(re.findall(self._float_string, fan_size)[0]))

    def _frequency_response(self, frequency_response: str):
        """
        Hidden function that retrieves frequency response data from a raw string.

        :param frequency_response: str: Raw frequency response data.
        :return: Result: Data object that represents frequency response data.
        """

        if frequency_response == "-":
            return Result(None)
        start, end = frequency_response.split("-")
        nums = [float(num) for num in re.findall(self._float_string, frequency_response)]
        if " kHz" in start:
            start = nums[0] * 1000
        else:
            start = nums[0]
        if " kHz" in end:
            end = nums[1] * 1000
        else:
            end = nums[1]
        return Result(FrequencyResponse(start, end, None))


    def _gpu_series(self, series: str):
        """
        Hidden function that veries that a given string is a valid GPU series.

        :param series: str: Raw series data.
        :return: Result: Verified GPU series data.
        """

        chipset_matches = [chipset for chipset in self._chipset_types if chipset in series]
        if not chipset_matches:
            return Result(series)
        return Result(None, iterate=0)

    def _gpu_chipset(self, chipset: str):
        """
        Hidden function that verifies and retrieves the GPU chipset type from a raw string.

        :param chipset: str: Raw GPU chipset data.
        :return: Result: Verified GPU chipset data.
        """

        for c in self._chipset_types:
            if c in chipset:
                return Result(chipset)

    def _grams(self, grams: str):
        """
        Function that retrieves gram amounts in integers from a raw string.

        :param grams: str: Raw gram data.
        :return: Result: Gram data.
        """

        if " mg" in grams:
            return Result(float(re.findall(self._float_string, grams)[0])/1000)
        elif " g" in grams:
            return Result(float(re.findall(self._float_string, grams)[0]))

    def _hdd_cache(self, hdd_cache):
        """
        Hidden function that retrieves byte data from a raw string.

        :param hdd_cache: str: Raw cache size string.
        :return: Result: Size of the HDD cache.
        """

        if not hdd_cache or self._currency_sign in hdd_cache:
            return Result(None, iterate=0)
        return Result(self._bytes(hdd_cache, result=False))

    def _hdd_data(self, hdd_data: str):
        """
        Hidden function that determines the type of the HDD and the platter RPM from a given string.

        :param hdd_data: str: Raw HDD data.
        :return: Result: (HDD type, platter RPM)
        """

        if "RPM" in hdd_data:
            hdd_type = "HDD"
            rpm = int(re.findall(self._float_string, hdd_data)[0])
            return Result((hdd_type, rpm), tuple=True)
        else:
            return Result((hdd_data, None), tuple=True)

    def _hdd_form_factor(self, hdd_ff: list):
        """
        Hidden function that takes two strings and returns the string that is a valid form factor.

        :param hdd_ff: list: List of two strings that contains raw HDD data.
        :return: Result: HDD form factor.
        """

        if hdd_ff[0] in self._hdd_form_factors:
            return Result(hdd_ff[0])
        return Result(hdd_ff[1])

    def _hdd_series(self, hdd_series: list):
        """
        Hidden function that examines a list of strings and returns a valid HDD series string.

        :param hdd_series: list: Raw HDD data
        :return: Result: The HDD series.
        """

        if hdd_series[0] in self._hdd_form_factors:
            if hdd_series[1] in self._hdd_form_factors:
                return Result(None)
            return Result(None, iterate=0)
        elif not hdd_series[1] in self._hdd_form_factors:
            return Result(" ".join(hdd_series), iterate=2)
        return Result(hdd_series[0])

    def _ips(self, ips: str):
        """
        Hidden function that retrieves an IPS value from the given raw string.

        :param ips: str: Raw IPS string.
        :return: Validated IPS string.
        """

        if not ips:
            return Result(None)
        try:
            return self._boolean(ips)
        except ValueError:
            if self._currency_sign in ips:
                return Result(None, iterate=0)

    def _interface(self, interface: str):
        """
        Hidden function that validates a given raw interface string.

        :param interface: str: Raw interface string.
        :return: Result: Validated interface string.
        """

        for inter in self._interface_types:
            if inter in interface:
                return Result(interface)

    def _kb_switches(self, switches: str):
        """
        Hidden function that validates a given keyboard switches string.

        :param switches: str: Raw keyboard switches string.
        :return: Result: Validated interface string.
        """

        if not switches or switches in self._backlight_types or self._currency_sign in switches:
            return Result(None, iterate=0)
        return Result(switches)

    def _kb_backlight(self, backlight: str):
        """
        Hidden function that validates a given backlight string.

        :param backlight: str: Raw backlight string.
        :return: Result: Validated backlight string.
        """

        if not backlight or not backlight in self._backlight_types:
            return Result(None, iterate=0)
        return Result(backlight)

    def _memory_sizes(self, memory_size: str):
        """
        Hidden function that parses memory size data.

        :param memory_size: str: Raw memory size data.
        :return: Result: (int, Bytes)
        """

        memory_data = memory_size.split("x")
        num_modules = int(memory_data[0])
        num_bytes = self._bytes(memory_data[1], result=False)
        return Result((num_modules, num_bytes), tuple=True)

    def _memory_type(self, type_data: str):
        """
        Hidden function that retrieves memory type and speed data from a raw string.

        :param type_data: str: Raw memory type data.
        :return: Result: (str, ClockSpeed)
        """
        type_data = type_data.split("-")
        module_type = type_data[0]
        speed = ClockSpeed.from_MHz(int(type_data[1]))
        return Result((module_type, speed), tuple=True)

    def _monitor_size(self, monitor_size: str):
        """
        Hidden function that returns the diagonal size of a monitor from a given string.

        :param monitor_size: str: Raw numeric string.
        :return: Result: Diagonal monitor size.
        """

        return Result(float(re.findall(self._float_string, monitor_size)[0]))

    def _network_speed(self, network_speed: str):
        """
        Hidden function that returns the network speed data from a raw string.

        :param network_speed: str: Raw network speed data.
        :return: Result: Data object that represents network speed.
        """

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
        return Result(None, iterate=0)

    def _psu_type(self, psu_type: str):
        """
        Hidden function that returns a validated PSU type string.

        :param psu_type: str: Raw psu string.
        :return: Result: Validated PSU type string.
        """

        if psu_type in self._psu_types:
            return Result(psu_type)

    def _psu_modular(self, psu_modularity: str):
        """
        Hidden function that returns a validated PSU modularity string.

        :param psu_modularity: str: Raw PSU modularity data.
        :return: Result: Validated PSU modularity string.
        """

        if psu_modularity in self._psu_modularity:
            return Result(psu_modularity)

    def _psu_series(self, series: list):
        """
        Hidden function that examines a list of raw strings and returns the string
        that resembles the series of the given PSU.

        :param series: list: The raw PSU data.
        :return: Result: Validated PSU series string.
        """

        psu_type = self._psu_type(series[0])
        if psu_type:
            if self._psu_type(series[1]):
                return Result(series[0])
            return Result(None, iterate=0)
        return Result(series[0])

    def _psu_efficiency(self, efficiency: str):
        """
        Hidden function that retrieves PSU efficiency data from a raw string.

        :param efficiency: str: Raw PSU efficiency data.
        :return: Result: Validated PSU efficiency string.
        """

        if efficiency == "-":
            return Result(None)
        elif "80+" in efficiency:
            return Result(efficiency)

    def _rd_speeds(self, rd_speed: str):
        """
        Hidden function that returns the read speed for an optical drive.

        :param rd_speed: str: Raw read speed data.
        :return: Result: Read speed value
        """

        if rd_speed == "-":
            return Result(None)
        return self._retrieve_int(rd_speed)

    def _resolution(self, resolution: str):
        """
        Hidden function that returns a Resolution data object from a raw string.

        :param resolution: str: Raw resolution data.
        :return: Result: Resolution data object.
        """

        width, height = resolution.split(" x ")
        return Result(Resolution(int(width), int(height)))

    def _response_time(self, response_time: str):
        """
        Hidden function that the response time from a raw string.

        :param response_time: str: Raw response time data.
        :return: Result: Response time value.
        """
        if response_time == "Yes" or response_time == "No":
            return Result(None)
        return Result(int(re.findall(self._float_string, response_time)[0]))

    def _sample_rate(self, sample_rate: str):
        """
        Hidden function that retrieves the sample rate from a raw string.

        :param sample_rate: str: Raw sample rate data.
        :return: Result: Parsed sample rate data.
        """

        if not sample_rate or self._currency_sign in sample_rate:
            return Result(None)
        return Result(float(re.findall(self._float_string, sample_rate)[0]))

    def _sound_card_chipset(self, sc_chipset: str):
        """
        Hidden function that returns chipset data from a given string.

        :param sc_chipset: str: Raw chipset data.
        :return: Result: Validated chipset string.
        """

        try:
            if float(sc_chipset):
                return Result(None, iterate=0)
        except ValueError:
            return Result(sc_chipset)

    def _snr(self, snr: str):
        """
        Hidden function that retrieves SNR data from a raw string.

        :param snr: str: Raw SNR data.
        :return: Result: Validated SNR value.
        """

        if not snr or self._currency_sign in snr or " kHz" in snr:
            return Result(None)
        return Result(int(re.findall(self._float_string, snr)[0]))

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
        for watt in self._watt_ratings:
            if watt in watt_string:
                num_string = re.findall(self._float_string, watt_string)[0]
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

    def _wireless_protocols(self, protocols: str):
        """
        Hidden function that retrieves validated wireless protocols from a raw string.

        :param protocols: str: Raw protocol data.
        :return: Result: Validated protocol data.
        """

        if [x for x in self._wireless_protocol_id if x in protocols]:
            return Result(protocols)

    def _wr_speeds(self, wr_speed: str):
        """
        Hidden function that validates optical drive read speeds from a raw string.

        :param wr_speed: str: Raw write speed data
        :return: Result: Validated write speed data.
        """

        if [x for x in wr_speed if x == "-"]:
            return Result(None)
        return Result(wr_speed)

    def _va(self, va):
        """
        Hidden function that retrieve volt-ampere data from a raw string.

        :param va: Raw VA data.
        :return: Result: VA data.
        """

        if not va or self._currency_sign in va:
            return Result(None, iterate=0)
        num = float(re.findall(self._float_string, va)[0])
        if " kVA" in va:
            num *= 1000
        return Result(int(num))


class Result:
    """Result:

    This class represents the result of the various parse functions in the Parser class. These functions
    contain data about how the rest of the parsing should proceed, and how the result data should be handled.
    """

    def __init__(self, value, iterate=1, tuple=False):
        self.value = value
        self.iterate = iterate
        self.tuple = tuple

    def __repr__(self):
        return f"Value: {self.value}, Iterate: {self.iterate}, Tuple: {self.tuple}"
