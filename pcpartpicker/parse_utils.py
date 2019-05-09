import logging
import re
from typing import Generator, List, Optional, Tuple, Union, Dict, Callable

from .brands import brands
from .mappings import byte_classes, clockspeeds
from .parts import Bytes, CFM, ClockSpeed, Decibels, FrequencyResponse, NetworkSpeed, Resolution, RPM
from .utils import retrieve_float, retrieve_int, num_pattern

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


def tokenize(part: str, tags: list) -> Generator[List[str], None, None]:
    """
    Hidden generator that yields up chunks of part data.

    :param part: str: The part name
    :param tags: list: The raw tags returned from the lxml parser.
    :return: List of individual part data.
    """

    chunk_length = len(part_funcs[part]) + 2
    for i in range(0, len(tags), chunk_length):
        yield tags[i:i + chunk_length]


def num(string: str) -> Optional[Union[float, int]]:
    """
    Hidden function that attempts to retrieve a numeric value from a string.

    :param string: str: The raw numeric string.
    :return: Result: The numeric value retrieved from the string.
    """

    if "." not in string:
        return retrieve_int(string)
    return retrieve_float(string)


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
    logger.debug(f"{bool_str} is not a valid boolean!")


def retrieve_brand_info(model_string: str) -> Tuple[Optional[str], Optional[str]]:
    for x in range(len(model_string) + 1):
        if model_string[:x] in brands:
            try:
                next_char = model_string[x]
                if not next_char == " ":
                    continue
                raise IndexError
            except IndexError:
                brand = model_string[:x].strip().lstrip()
                model = model_string[x:].strip().lstrip()
                if not model:
                    return brand, None
                else:
                    return brand, model
    logger.warning(f"Could not find brand in {model_string}!")
    return None, model_string


def core_clock(clock_data: str) -> Optional[ClockSpeed]:
    """
    Hidden function that extracts core clock data from a raw string.

    :param clock_data: str: Raw core clock string.
    :return: Result: A ClockSpeed data object generated from the string.
    """

    for speed_type, func in clockspeeds.items():
        if speed_type in clock_data:
            clock_number = retrieve_float(clock_data)
            return func(clock_number)
    logger.debug(f"Could not find clock speed data for {clock_data}.")


def decibels(decibel_data: str) -> Decibels:
    """
    Hidden function that retrieves decibel data from a raw string.

    :param decibel_data: Raw decibel data.
    :return: Result: Decibels data object generated from the raw string.
    """

    num_strings: List[str] = re.findall(num_pattern, decibel_data)
    nums: List[float] = [float(number) for number in num_strings]
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

    nums: List[float] = [float(number) for number in re.findall(num_pattern, cfm)]
    if len(nums) == 2:
        return CFM(nums[0], nums[1], None)
    if len(nums) == 1:
        return CFM(None, None, nums[0])
    logger.debug(f"No valid CFM data found in {cfm}.")


def fan_rpm(rpm: str) -> Optional[RPM]:
    """
    Hidden function that returns fan rpm data from a raw string.

    :param rpm: str: Raw fan data.
    :return: Result: Data object representing fan RPM.
    """

    nums = re.findall(num_pattern, rpm)
    nums = [int(number) for number in nums]
    if len(nums) == 2:
        return RPM(nums[0], nums[1], None)
    if len(nums) == 1:
        return RPM(None, None, nums[0])
    logger.debug(f"Could not find valid RPM data for {rpm}.")


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


def hdd_data(data: str) -> Tuple[Optional[str], Optional[int]]:
    """
    Hidden function that determines the type of the HDD and the platter RPM from a given string.

    :param data: str: Raw HDD data.
    :return: Result: (HDD type, platter RPM)
    """

    if data is None:
        return None, None
    elif data == "SSD" or data == "Hybrid":
        return data, None
    elif "RPM" in data:
        hdd_type = "HDD"
        rpm = retrieve_int(data)
        return hdd_type, rpm
    logger.debug(f"Could not find HDD type and RPM in {data}!")


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
    speed = ClockSpeed.from_mhz(int(type_data[1]))
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
            return NetworkSpeed.from_mbits(freq), 1
        else:
            return NetworkSpeed.from_mbits(freq), int(speed_port_info[1])
    else:
        if len(speed_port_info) == 1:
            return NetworkSpeed.from_gbits(freq), 1
        else:
            return NetworkSpeed.from_gbits(freq), int(speed_port_info[1])


def price(data: str) -> str:
    """
    Internal method that is designed to signal to the parser that this is a price string.
    :param data:
    :return:
    """
    return data


def resolution(res_str: str) -> Resolution:
    """
    Hidden function that returns a Resolution data object from a raw string.

    :param res_str: str: Raw resolution data.
    :return: Result: Resolution data object.
    """

    width, height = res_str.split(" x ")
    return Resolution(int(width), int(height))


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
    logger.debug(f"Could not find a valid byte value in {byte_string}.")


def wr_speeds(wr_speed: str) -> Optional[str]:
    """
    Hidden function that validates optical drive read speeds from a raw string.

    :param wr_speed: str: Raw write speed data
    :return: Optional[str]: Validated write speed data.
    """

    if [x for x in wr_speed if x == "-"]:
        return None
    return wr_speed


def wattage(watt_string: str) -> Union[float, int]:
    """
    Hidden function that retrieves watt data from a given string.

    Note: This function coerces all watt values to watts, as there is a fair bit of erroneous
    data on PCPartPicker.

    :param watt_string: str:
    :return: int: Watt value.
    """

    num_string = re.findall(num_pattern, watt_string)[0]
    number = float(num_string)
    if " kW" in watt_string:
        number *= 1000
    return int(number)


def va(va_data: str) -> float:
    """
    Hidden function that retrieve volt-ampere data from a raw string.

    :param va_data: Raw VA data.
    :return: int: VA data.
    """

    number = retrieve_float(va_data)
    if " kVA" in va_data:
        number *= 1000.0
    return number


part_funcs: Dict[str, List[Callable]] = {
    "cpu": [int, core_clock, core_clock, wattage, default, boolean],
    "cpu-cooler": [fan_rpm, decibels, default, retrieve_int],
    "motherboard": [default, default, int, to_bytes, default],
    "memory": [memory_type, default, memory_sizes, price, default, int],
    "internal-hard-drive": [to_bytes, price, hdd_data, to_bytes, default, default],
    "video-card": [default, to_bytes, core_clock, core_clock, default, default],
    "power-supply": [default, default, wattage, default, default],
    "case": [default, default, wattage, boolean, int, int],
    "case-fan": [retrieve_int, default, fan_rpm, fan_cfm, decibels, boolean],
    "fan-controller": [int, wattage, boolean, default, default],
    "thermal-paste": [grams],
    "optical-drive": [int, int, int, wr_speeds,
                      wr_speeds, wr_speeds],
    "sound-card": [retrieve_float, num, retrieve_int, retrieve_float, default, default],
    "wired-network-card": [default, network_speed, default],
    "wireless-network-card": [default, default, default],
    "monitor": [num, resolution, retrieve_int, retrieve_int, default, default],
    "external-hard-drive": [default, default, to_bytes, price, default, hdd_data],
    "headphones": [default, frequency_response, boolean, boolean, default, default],
    "keyboard": [default, default, default, boolean, default, default],
    "mouse": [default, default, int, default, default],
    "speakers": [retrieve_float, wattage, frequency_response, default],
    "ups": [wattage, va]
}
