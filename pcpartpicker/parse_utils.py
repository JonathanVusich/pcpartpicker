from itertools import islice
import logging
import re
from typing import Optional

from .mappings import backlights, bitrates, byte_classes, cases, colors, gpu_chipsets, hdd_form_factors, \
    mobo_interfaces, net_speeds, num_pattern, psu_form_factors, psu_modularity_options, wifi_protocol
from .parts import CFM, ClockSpeed, FrequencyResponse, NetworkSpeed, Resolution, RPM


logger = logging.getLogger(__name__)


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


def retrieve_data(tags: list):
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
                start_index += y + 1
                break
        if not it:
            return
        yield it


def retrieve_int(string: str):
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


def retrieve_float(string: str):
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


def retrieve_num(string: str):
    """
    Hidden function that attempts to retrieve a numeric value from a string.

    :param string: str: The raw numeric string.
    :return: Result: The numeric value retrieved from the string.
    """

    try:
        return retrieve_int(string)
    except ValueError:
        try:
            return retrieve_float(string)
        except ValueError:
            raise ValueError("Not a valid numeric string!")


def to_bytes(byte_string: str, result=True):
    """
    Hidden function that parses a string representing binary size to a Bytes data object.

    :param byte_string: str: The raw string representing binary size.
    :param result: Determines whether or not the return type of this function should be a
    Result object or the Bytes object.
    :return: Result, Bytes:
    """

    if not byte_string:
        return Result(None)
    for byte_type, func in byte_classes.items():
        if byte_type in byte_string:
            byte_num = float(re.findall(num_pattern, byte_string)[0])
            if result:
                return Result(func(byte_num))
            return func(byte_num)


def boolean(bool_str: str):
    """
    Hidden function that returns a boolean value from a string.

    :param bool_str: str: The raw boolean string.
    :return: Result: The boolean value extracted from the string.
    """

    if bool_str == "Yes":
        return Result(True)
    elif bool_str == "No":
        return Result(False)
    raise ValueError("Not a valid boolean!")


def audio_bitrate(audio_br: str):
    """
    Hidden function that extract audio bitrate data from a string.

    :param audio_br: str: The raw audio bitrate string.
    :return: Result: The audio bitrate extracted from the string
    """
    if audio_br == "None":
        return Result(None)
    if audio_br in bitrates:
        return Result(int(audio_br))
    else:
        logger.debug(f"Audio bitrate {audio_br} is undefined in mappings!")


def case_type(case: str):
    """
    Hidden function that returns the case type string if it is of a valid type.

    :param case: str: The raw case type string.
    :return: Result: The verified case type.
    """

    if case in cases:
        return Result(case)
    else:
        logger.debug(f"Case type {case} is undefined in mappings!")


def color(color_str: str):
    """
    Hidden function that returns the given string if is a valid color.

    :param color_str: str: The raw color string.
    :return: Result: The verified color string.
    """
    if not color_str or color_str not in colors:
        return Result(None, iterate=0)
    return Result(color_str)


def default(default_str: str):
    """
    Placeholder function that simply returns the string as is.

    :param default_str: str: The default string
    :return: Result: The default string.
    """

    return Result(default_str)


def external_hdd_series(series: str) -> Result:
    """
    Hidden function that verifies that the given string is a compatible external HDD type.

    :param series: str: Raw HDD type.
    :return: Result: The verified HDD type.
    """

    if series == "Desktop" or series == "Portable":
        return Result(None, iterate=0)
    return Result(series)


def fan_cfm(cfm: str):
    """
    Hidden function that generates fan airflow data from a raw string.

    :param cfm: str: The raw airflow data.
    :return: Result: Data object representing airflow data.
    """

    if cfm == "N/A":
        return Result(None)
    nums = [float(num) for num in re.findall(num_pattern, cfm)]
    if len(nums) == 2:
        return Result(CFM(nums[0], nums[1], None))
    if len(nums) == 1:
        return Result(CFM(None, None, nums[0]))
    logger.warning(f"No valid CFM data found in {cfm}.")


def fan_color(color_str: str) -> Result:
    """
    Hidden function that checks fan color validity.

    :param color_str: str: Raw color string.
    :return: Result: Validated color string.
    """

    if fan_size(color_str):
        return Result(None, iterate=0)
    return Result(color_str)


def fan_rpm(rpm: str):
    """
    Hidden function that returns fan rpm data from a raw string.

    :param rpm: str: Raw fan data.
    :return: Result: Data object representing fan RPM.
    """

    if not rpm or rpm == "N/A" or rpm == "-":
        return Result(None)
    nums = re.findall(num_pattern, rpm)
    nums = [int(num) for num in nums]
    if "-" in rpm:
        if len(nums) == 2:
            return Result(RPM(nums[0], nums[1], None))
        raise ValueError("Not a valid number of numeric values!")
    if len(nums) == 1:
        return Result(RPM(None, None, nums[0]))
    raise ValueError("Not a valid number of numeric values!")


def fan_size(size: str):
    """
    Hidden function that retrieves fan size in integers from a raw string.

    :param size: str: Raw fan size data.
    :return: Result: Fan size in mm.
    """

    if "mm" in size and len([x for x in size if x.isnumeric()]) > 1:
        return Result(int(re.findall(num_pattern, size)[0]))
    else:
        logger.debug(f"Could not find fan size for {size}.")


def frequency_response(response: str):
    """
    Hidden function that retrieves frequency response data from a raw string.

    :param response: str: Raw frequency response data.
    :return: Result: Data object that represents frequency response data.
    """

    if response == "-":
        return Result(None)
    start, end = response.split("-")
    nums = [float(num) for num in re.findall(num_pattern, response)]
    if " kHz" in start:
        start = nums[0] * 1000
    else:
        start = nums[0]
    if " kHz" in end:
        end = nums[1] * 1000
    else:
        end = nums[1]
    return Result(FrequencyResponse(start, end, None))


def gpu_series(series: str) -> Result:
    """
    Hidden function that verifies that a given string is a valid GPU series.

    :param series: str: Raw series data.
    :return: Result: Verified GPU series data.
    """

    chipset_matches = [chipset for chipset in gpu_chipsets if chipset in series]
    if not chipset_matches:
        return Result(series)
    return Result(None, iterate=0)


def gpu_chipset(chipset: str):
    """
    Hidden function that verifies and retrieves the GPU chipset type from a raw string.

    :param chipset: str: Raw GPU chipset data.
    :return: Result: Verified GPU chipset data.
    """

    for c in gpu_chipsets:
        if c in chipset:
            return Result(chipset)
    logger.warning(f"Could not find a valid GPU chipset for {chipset}.")


def grams(data: str):
    """
    Function that retrieves gram amounts in integers from a raw string.

    :param data: str: Raw gram data.
    :return: Result: Gram data.
    """

    if " mg" in data:
        return Result(float(re.findall(num_pattern, data)[0]) / 1000)
    elif " g" in data:
        return Result(float(re.findall(num_pattern, data)[0]))


def hdd_data(data: str):
    """
    Hidden function that determines the type of the HDD and the platter RPM from a given string.

    :param data: str: Raw HDD data.
    :return: Result: (HDD type, platter RPM)
    """

    if "RPM" in data:
        hdd_type = "HDD"
        rpm = int(re.findall(num_pattern, data)[0])
        return Result((hdd_type, rpm), tuple=True)
    else:
        return Result((data, None), tuple=True)


def hdd_form_factor(hdd_ff: list):
    """
    Hidden function that takes two strings and returns the string that is a valid form factor.

    :param hdd_ff: list: List of two strings that contains raw HDD data.
    :return: Result: HDD form factor.
    """

    if hdd_ff[0] in hdd_form_factors:
        return Result(hdd_ff[0])
    return Result(hdd_ff[1])


def hdd_series(hdd_data: list):
    """
    Hidden function that examines a list of strings and returns a valid HDD series string.

    :param hdd_data: list: Raw HDD data
    :return: Result: The HDD series.
    """

    if hdd_data[0] in hdd_form_factors:
        if hdd_data[1] in hdd_form_factors:
            return Result(None)
        return Result(None, iterate=0)
    elif not hdd_data[1] in hdd_form_factors:
        return Result(" ".join(hdd_data), iterate=2)
    return Result(hdd_data[0])


def interface(ifc: str) -> Optional[Result]:
    """
    Hidden function that validates a given raw interface string.

    :param ifc: str: Raw interface string.
    :return: Result: Validated interface string.
    """

    for inter in mobo_interfaces:
        if inter in ifc:
            return Result(ifc)


def kb_backlight(backlight: str):
    """
    Hidden function that validates a given backlight string.

    :param backlight: str: Raw backlight string.
    :return: Result: Validated backlight string.
    """

    if not backlight or backlight not in backlights:
        return Result(None, iterate=0)
    return Result(backlight)


def memory_sizes(memory_size: str):
    """
    Hidden function that parses memory size data.

    :param memory_size: str: Raw memory size data.
    :return: Result: (int, Bytes)
    """

    memory_data = memory_size.split("x")
    num_modules = int(memory_data[0])
    num_bytes = to_bytes(memory_data[1], result=False)
    return Result((num_modules, num_bytes), tuple=True)


def memory_type(type_data: str):
    """
    Hidden function that retrieves memory type and speed data from a raw string.

    :param type_data: str: Raw memory type data.
    :return: Result: (str, ClockSpeed)
    """
    type_data = type_data.split("-")
    module_type = type_data[0]
    speed = ClockSpeed.from_MHz(int(type_data[1]))
    return Result((module_type, speed), tuple=True)


def monitor_size(size: str):
    """
    Hidden function that returns the diagonal size of a monitor from a given string.

    :param size: str: Raw numeric string.
    :return: Result: Diagonal monitor size.
    """

    return Result(float(re.findall(num_pattern, size)[0]))


def network_speed(data: str):
    """
    Hidden function that returns the network speed data from a raw string.

    :param data: str: Raw network speed data.
    :return: Result: Data object that represents network speed.
    """

    compatible_speeds = [
        speed
        for speed in net_speeds
        if speed in data
    ]
    if compatible_speeds:
        speed = re.findall(num_pattern, data)
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


def psu_type(psu_str: str):
    """
    Hidden function that returns a validated PSU type string.

    :param psu_str: str: Raw psu string.
    :return: Result: Validated PSU type string.
    """

    if psu_str in psu_form_factors:
        return Result(psu_str)
    else:
        logger.debug(f"Could not find a PSU type for {psu_str}.")


def psu_modular(psu_modularity: str):
    """
    Hidden function that returns a validated PSU modularity string.

    :param psu_modularity: str: Raw PSU modularity data.
    :return: Result: Validated PSU modularity string.
    """

    if psu_modularity in psu_modularity_options:
        return Result(psu_modularity)
    else:
        logger.debug(f"Could not find a valid PSU type for {psu_modularity}.")


def psu_efficiency(efficiency: str) -> Result:
    """
    Hidden function that retrieves PSU efficiency data from a raw string.

    :param efficiency: str: Raw PSU efficiency data.
    :return: Result: Validated PSU efficiency string.
    """

    if efficiency == "-":
        return Result(None)
    elif "80+" in efficiency:
        return Result(efficiency)


def psu_series(series: list):
    """
    Hidden function that examines a list of raw strings and returns the string
    that resembles the series of the given PSU.

    :param series: list: The raw PSU data.
    :return: Result: Validated PSU series string.
    """

    ptype = psu_type(series[0])
    if ptype:
        if psu_type(series[1]):
            return Result(series[0])
        return Result(None, iterate=0)
    return Result(series[0])


def rd_speeds(rd_speed: str):
    """
    Hidden function that returns the read speed for an optical drive.

    :param rd_speed: str: Raw read speed data.
    :return: Result: Read speed value
    """

    if rd_speed == "-":
        return Result(None)
    return retrieve_int(rd_speed)


def resolution(res_str: str) -> Result:
    """
    Hidden function that returns a Resolution data object from a raw string.

    :param res_str: str: Raw resolution data.
    :return: Result: Resolution data object.
    """

    width, height = res_str.split(" x ")
    return Result(Resolution(int(width), int(height)))


def response_time(response_str: str) -> Result:
    """
    Hidden function that the response time from a raw string.

    :param response_str: str: Raw response time data.
    :return: Result: Response time value.
    """
    if response_str == "Yes" or response_str == "No":
        return Result(None)
    return Result(int(re.findall(num_pattern, response_str)[0]))


def sound_card_chipset(sc_chipset: str):
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


def wireless_protocols(protocols: str) -> Optional[Result]:
    """
    Hidden function that retrieves validated wireless protocols from a raw string.

    :param protocols: str: Raw protocol data.
    :return: Result: Validated protocol data.
    """

    if [x for x in wifi_protocol if x in protocols]:
        return Result(protocols)


def wr_speeds(wr_speed: str) -> Result:
    """
    Hidden function that validates optical drive read speeds from a raw string.

    :param wr_speed: str: Raw write speed data
    :return: Result: Validated write speed data.
    """

    if [x for x in wr_speed if x == "-"]:
        return Result(None)
    return Result(wr_speed)
