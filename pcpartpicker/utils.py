import re
from typing import Union

num_pattern = r"(?<![a-zA-Z:])[-+]?\d*\.?\d+"


def retrieve_float(data: str) -> float:
    """
    Function that returns a float from a random data string.
    :param data:
    :return:
    """

    try:
        return float(re.findall(num_pattern, data)[0])
    except IndexError:
        raise ValueError


def retrieve_int(data: str) -> int:
    """
    Function that returns an int from a random data string.
    :param data:
    :return:
    """

    try:
        return int(re.findall(num_pattern, data)[0])
    except IndexError:
        raise ValueError


def num(string: str) -> Union[float, int]:
    """
    Hidden function that attempts to retrieve a numeric value from a string.

    :param string: str: The raw numeric string.
    :return: Result: The numeric value retrieved from the string.
    """

    if "." not in string:
        return retrieve_int(string)
    return retrieve_float(string)
