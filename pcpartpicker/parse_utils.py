from itertools import islice
import logging
import re
from typing import Generator, List, Optional, Tuple

from .mappings import byte_classes, clockspeeds, hdd_form_factors, num_pattern, \
    psu_form_factors, psu_modularity_options
from .parts import Bytes, CFM, ClockSpeed, Decibels, FrequencyResponse, NetworkSpeed, Resolution, RPM


logger = logging.getLogger(__name__)


def tokenize(part: str, tags: list) -> Generator:
    """
    Hidden generator that yields up chunks of part data.

    :param part: str: The part name
    :param tags: list: The raw tags returned from the lxml parser.
    :return: List of individual part data.
    """

    chunk_length = len(part_funcs[part]) + 2
    for i in range(0, len(tags), chunk_length):
        yield tags[i:i + chunk_length]


def num(string: str):
    """
    Hidden function that attempts to retrieve a numeric value from a string.

    :param string: str: The raw numeric string.
    :return: Result: The numeric value retrieved from the string.
    """

    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            raise ValueError("Not a valid numeric string!")


def boolean(bool_str: str) -> Optional[bool]:
    """
    Hidden function that returns a boolean value from a string.

    :param bool_str: str: The raw boolean string.
    :return: Result: The boolean value extracted from the string.
    """

    if bool_str == "Yes":
        return True
    elif bool_str == "No":
        return False
    raise ValueError("Not a valid boolean!")


def core_clock(clock_data: str):
    """
    Hidden function that extracts core clock data from a raw string.

    :param clock_data: str: Raw core clock string.
    :return: Result: A ClockSpeed data object generated from the string.
    """

    for speed_type, func in clockspeeds.items():
        if speed_type in clock_data:
            clock_number = float(re.findall(num_pattern, clock_data)[0])
            return func(clock_number)
    logger.warning(f"Could not find clock speed data for {clock_data}.")


def decibels(decibel_data: str) -> Decibels:
    """
    Hidden function that retrieves decibel data from a raw string.

    :param decibel_data: Raw decibel data.
    :return: Result: Decibels data object generated from the raw string.
    """

    num_strings: List[str] = re.findall(num_pattern, decibel_data)
    nums: List[float] = [float(number) for number in num_strings]
    if "-" in decibel_data:
        if len(nums) == 2:
            return Decibels(nums[0], nums[1], None)
    return Decibels(None, None, nums[0])


def default(default_str: str) -> str:
    """
    Placeholder function that simply returns the string as is.

    :param default_str: str: The default string
    :return: str: The default string.
    """

    return default_str


def fan_cfm(cfm: str) -> Optional[CFM]:
    """
    Hidden function that generates fan airflow data from a raw string.

    :param cfm: str: The raw airflow data.
    :return: Result: Data object representing airflow data.
    """

    nums = [float(number) for number in re.findall(num_pattern, cfm)]
    if len(nums) == 2:
        return CFM(nums[0], nums[1], None)
    if len(nums) == 1:
        return CFM(None, None, nums[0])
    logger.warning(f"No valid CFM data found in {cfm}.")


def fan_rpm(rpm: str) -> Optional[RPM]:
    """
    Hidden function that returns fan rpm data from a raw string.

    :param rpm: str: Raw fan data.
    :return: Result: Data object representing fan RPM.
    """

    nums = re.findall(num_pattern, rpm)
    nums = [int(number) for number in nums]
    if "-" in rpm:
        if len(nums) == 2:
            return RPM(nums[0], nums[1], None)
        raise ValueError("Not a valid number of numeric values!")
    if len(nums) == 1:
        return RPM(None, None, nums[0])
    raise ValueError("Not a valid number of numeric values!")


def frequency_response(response: str) -> FrequencyResponse:
    """
    Hidden function that retrieves frequency response data from a raw string.

    :param response: str: Raw frequency response data.
    :return: Result: Data object that represents frequency response data.
    """

    start, end = response.split("-")
    nums = [float(number) for number in re.findall(num_pattern, response)]
    if " kHz" in start:
        start = nums[0] * 1000
    else:
        start = nums[0]
    if " kHz" in end:
        end = nums[1] * 1000
    else:
        end = nums[1]
    return FrequencyResponse(start, end, None)


def grams(data: str) -> float:
    """
    Function that retrieves gram amounts in integers from a raw string.

    :param data: str: Raw gram data.
    :return: float: Gram data.
    """

    if " mg" in data:
        return retrieve_float(data) / 1000
    return retrieve_float(data)


def hdd_data(data: str) -> Tuple[str, Optional[int]]:
    """
    Hidden function that determines the type of the HDD and the platter RPM from a given string.

    :param data: str: Raw HDD data.
    :return: Result: (HDD type, platter RPM)
    """

    if "RPM" in data:
        hdd_type = "HDD"
        rpm = int(re.findall(num_pattern, data)[0])
        return hdd_type, rpm
    else:
        return data, None


def hdd_series(hdd_data: list):
    """
    Hidden function that examines a list of strings and returns a valid HDD series string.

    :param hdd_data: list: Raw HDD data
    :return: Result: The HDD series.
    """

    if hdd_data[0] in hdd_form_factors:
        if hdd_data[1] in hdd_form_factors:
            return None
    elif not hdd_data[1] in hdd_form_factors:
        return " ".join(hdd_data)
    return hdd_data[0]


def memory_sizes(memory_size: str) -> Tuple[int, Bytes]:
    """
    Hidden function that parses memory size data.

    :param memory_size: str: Raw memory size data.
    :return: Result: (int, Bytes)
    """

    memory_data = memory_size.split("x")
    num_modules = int(memory_data[0])
    num_bytes = to_bytes(memory_data[1])
    return num_modules, num_bytes


def memory_type(type_data: str) -> Tuple[str, ClockSpeed]:
    """
    Hidden function that retrieves memory type and speed data from a raw string.

    :param type_data: str: Raw memory type data.
    :return: Result: (str, ClockSpeed)
    """
    type_data = type_data.split("-")
    module_type = type_data[0]
    speed = ClockSpeed.from_MHz(int(type_data[1]))
    return module_type, speed


def network_speed(data: str) -> Tuple[NetworkSpeed, int]:
    """
    Hidden function that returns the network speed data from a raw string.

    :param data: str: Raw network speed data.
    :return: Result: Data object that represents network speed.
    """

    speed_port_info = re.findall(num_pattern, data)
    freq = int(speed_port_info[0])
    if "Mbit/s" in data:
        if len(speed_port_info) == 1:
            return NetworkSpeed.from_Mbits(freq), 1
        else:
            return NetworkSpeed.from_Mbits(freq), int(speed_port_info[1])
    else:
        if len(speed_port_info) == 1:
            return NetworkSpeed.from_Gbits(freq), 1
        else:
            return NetworkSpeed.from_Gbits(freq), int(speed_port_info[1])


def psu_type(psu_str: str) -> Optional[str]:
    """
    Hidden function that returns a validated PSU type string.

    :param psu_str: str: Raw psu string.
    :return: Result: Validated PSU type string.
    """

    if psu_str in psu_form_factors:
        return psu_str
    return None


def psu_modular(psu_modularity: str) -> Optional[str]:
    """
    Hidden function that returns a validated PSU modularity string.

    :param psu_modularity: str: Raw PSU modularity data.
    :return: Optional[str]: Validated PSU modularity string.
    """

    if psu_modularity in psu_modularity_options:
        return psu_modularity
    logger.debug(f"Could not find a valid PSU type for {psu_modularity}.")


def psu_series(data: str) -> Optional[str]:
    """
    Hidden function that examines a list of raw strings and returns the string
    that resembles the series of the given PSU.

    :param data: str: The raw PSU data.
    :return: Optional[str]: Validated PSU series string.
    """

    if psu_type(data):
        return None
    return data


def resolution(res_str: str) -> Resolution:
    """
    Hidden function that returns a Resolution data object from a raw string.

    :param res_str: str: Raw resolution data.
    :return: Result: Resolution data object.
    """

    width, height = res_str.split(" x ")
    return Resolution(int(width), int(height))


def retrieve_float(data: str) -> float:
    """
    Function that returns a float from a random data string.
    :param data:
    :return:
    """

    return float(re.findall(num_pattern, data)[0])


def retrieve_int(data: str) -> int:
    """
    Function that returns an int from a random data string.
    :param data:
    :return:
    """

    return int(re.findall(num_pattern, data)[0])


def to_bytes(byte_string: str) -> Optional[Bytes]:
    """
    Hidden function that parses a string representing binary size to a Bytes data object.

    :param byte_string: str: The raw string representing binary size.
    :return: Optional[Bytes]: a Bytes object representing the binary size of the given string.
    """

    for byte_type, func in byte_classes.items():
        if byte_type in byte_string:
            byte_num = float(re.findall(num_pattern, byte_string)[0])
            return func(byte_num)
    logger.warning(f"Could not find a valid byte value in {byte_string}.")


def wr_speeds(wr_speed: str) -> Optional[str]:
    """
    Hidden function that validates optical drive read speeds from a raw string.

    :param wr_speed: str: Raw write speed data
    :return: Optional[str]: Validated write speed data.
    """

    if [x for x in wr_speed if x == "-"]:
        return None
    return wr_speed


def wattage(watt_string: str) -> int:
    """
    Hidden function that retrieves watt data from a given string.

    Note: This function coerces all watt values to watts, as there is a fair bit of erroneous
    data on PCPartPicker.

    :param watt_string: str:
    :return: int: Watt value.
    """

    num_string = re.findall(num_pattern, watt_string)[0]
    try:
        number = int(num_string)
        if " kW" in watt_string:
            number *= 1000
        return number
    except ValueError:
        number = float(num_string)
        if " kW" in watt_string:
            number *= 1000
        return int(number)


def va(va_data: str):
    """
    Hidden function that retrieve volt-ampere data from a raw string.

    :param va_data: Raw VA data.
    :return: int: VA data.
    """

    number = float(re.findall(num_pattern, va_data)[0])
    if " kVA" in va:
        number *= 1000
    return int(number)


part_funcs = {
              "cpu": [core_clock, int, wattage],
              "cpu-cooler": [fan_rpm, decibels],
              "motherboard": [default, default, int, to_bytes],
              "memory": [memory_type, default, int,
                         memory_sizes, to_bytes],
              "internal-hard-drive": [default, default, hdd_data,
                                      to_bytes, to_bytes],
              "video-card": [default, default, to_bytes, core_clock],
              "power-supply": [psu_series, psu_type, default, wattage,
                               psu_modular],
              "case": [default, int, int, wattage],
              "case-fan": [default, retrieve_int, fan_rpm, fan_cfm,
                           decibels],
              "fan-controller": [default, int, wattage],
              "thermal-paste": [grams],
              "optical-drive": [int, int, int, wr_speeds,
                                wr_speeds, wr_speeds],
              "sound-card": [default, num, int,
                             float, retrieve_float],
              "wired-network-card": [default, network_speed],
              "wireless-network-card": [default, default],
              "monitor": [resolution, float, retrieve_int, boolean],
              "external-hard-drive": [default, default,
                                      to_bytes],
              "headphones": [default, boolean, boolean, frequency_response],
              "keyboard": [default, default, default, default],
              "mouse": [default, default, default],
              "speakers": [num, wattage, frequency_response],
              "ups": [wattage, va]
              }
