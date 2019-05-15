import logging
import re
from typing import List, Tuple, Optional

import lxml.html
from moneyed import USD

from .mappings import currency_classes, currency_symbols, part_classes, \
    none_symbols
from .parse_utils import tokenize, part_funcs, retrieve_brand_info
from .parts import *
from .utils import num_pattern

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class Parser:
    """Parser:

    This class is designed to parse raw html from PCPartPicker and to transform it into useful data objects.
    """

    _currency_sign: str = "$"

    _currency = USD

    _region: str = "us"

    def __init__(self, region: str = 'us') -> None:
        self._region = region
        self._currency_sign = currency_symbols[self._region]
        self._currency = currency_classes[self._region]

    def parse(self, parse_args: Tuple[str, List[str]]) -> Tuple[str, List]:
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
            tokens = list(tokenize(part, page))
            for token in tokens:
                part_list.append(self._parse_token(part, token))
        part_list.sort(
            key=lambda x: (x.brand if x.brand is not None else "", x.model if isinstance(x.model, str) else ""))
        return part, part_list

    def _parse_token(self, part: str, data: list) -> object:
        """
        Hidden function that parses a list of data depending on the part type.

        :param part: str: The part type of the accompanying data.
        :param data: list: A list of the raw string data for the given part.
        :return: Object: Parsed data object.
        """

        brand, model = retrieve_brand_info(data[0])
        parsed_data = [brand, model]
        price = self._price(data[-1])
        tokens = data[1:-1]

        for x, token in enumerate(tokens):
            func = part_funcs[part][x]
            if func.__name__ == "hdd_data":  # Handle special case of hdd_data input being None
                parsed_data.extend(func(token))
                continue
            elif func.__name__ == "price":  # Handle special case of price data being None
                parsed_data.append(self._price(token))
                continue
            else:
                if not token or token in none_symbols:
                    parsed_data.append(None)
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

    def _price(self, price: str) -> Money:
        """
        Hidden function that retrieves the price from a raw string.

        :param price: str: Raw string containing currency amount and info.
        :return: Result: Money object extracted from the string.
        """

        if not price:
            return Money("0.00", self._currency)
        elif [x for x in self._currency_sign if x in price]:
            return Money(re.findall(num_pattern, price)[0], self._currency)


def html_to_tokens(parse_args: Tuple[str, List[str]]) -> Tuple[str, List[List[str]]]:
    part, raw_html = parse_args
    html = [lxml.html.fromstring(html) for html in raw_html]
    tags = [page.xpath(
        'tr/td/a/div[@class="td__nameWrapper"]/p | tr/td[contains(@class, "td__spec")] | tr/td[@class="td__price"]')
        for page in html]
    return part, [parse_elements(elements) for elements in tags]


def parse_elements(elements: list) -> List[Optional[str]]:
    text_elements = []
    for element in elements:
        text = element.xpath("text()")
        if len(text) == 0:
            text_elements.append(None)
        elif len(text) == 1:
            text_elements.extend(text)
        else:
            element_string = " ".join(text)
            text_elements.append(element_string)
    return text_elements
