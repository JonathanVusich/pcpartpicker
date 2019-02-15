import logging
import re
from typing import List, Tuple, Generator

import lxml.html
from moneyed import USD

from .mappings import currency_classes, currency_symbols, part_classes, \
    none_symbols
from .parse_utils import tokenize, part_funcs
from .parts import *
from .utils import num_pattern

logger = logging.getLogger(__name__)


class Parser:
    """Parser:

    This class is designed to parse raw html from PCPartPicker and to transform it into useful data objects.
    """

    _currency_sign = "$"

    _currency = USD

    _region = "us"

    def __init__(self, region: str = 'us'):
        self._region = region
        self._currency_sign = currency_symbols[self._region]
        self._currency = currency_classes[self._region]

    def parse(self, parse_args: Tuple[str, List[str]]) -> tuple:
        """
        Hidden function that parses lists of raw html and returns useful data objects.

        :param parse_args: tuple: The first element of this tuple is the part type that is being parsed,
        the second element is the list of raw html data.
        :return: tuple: The first element of this tuple contains the part type of the parsed data, the
        second element is the list of parsed data objects.
        """

        part, tags = html_to_tokens(parse_args)
        part_list = []
        for page in tags:
            for token in tokenize(part, page):
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

        parsed_data = [data.pop(0)]
        price = self._price(data.pop(-1))

        for x, token in enumerate(data):
            if not token or token in none_symbols:
                parsed_data.append(None)
                continue
            func = part_funcs[part][x]
            # Check if this is a price function
            if func.__name__ == "price":
                parsed_data.append(self._price(token))
                continue
            result = func(token)
            if isinstance(result, tuple):
                parsed_data.extend(result)
            else:
                parsed_data.append(result)

        parsed_data.append(price)

        _class = part_classes[part]
        try:
            return _class(*parsed_data)
        except (TypeError, ValueError) as _:
            logger.error(f"{parsed_data} is not valid input data for {_class}!")

    def _price(self, price: str):
        """
        Hidden function that retrieves the price from a raw string.

        :param price: str: Raw string containing currency amount and info.
        :return: Result: Money object extracted from the string.
        """

        if not price:
            return Money("0.00", self._currency)
        elif [x for x in self._currency_sign if x in price]:
            return Money(re.findall(num_pattern, price)[0], self._currency)


def html_to_tokens(parse_args: Tuple[str, List[str]]) -> Tuple[str, Generator[List[str], None, None]]:
    part, raw_html = parse_args
    html = [lxml.html.fromstring(html) for html in raw_html]
    tags = [page.xpath('tr/td/a[not(text() = "Add")] | tr/td[not(a) and not(div) and not(input)]')
            for page in html]
    return part, ([tag.text for tag in page] for page in tags)
