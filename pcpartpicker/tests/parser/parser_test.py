import pytest
import json
from ...parse_utils import tokenize

from pcpartpicker.parser import Parser
from pcpartpicker.parts import *
from moneyed import Money, USD, INR, SEK, EUR, GBP


@pytest.fixture
def raw_html():
    return ("cpu", [{"html": "<tr><td class=\"select\"><input type=\"checkbox\" class=\"px\" id=\"px_171631\"></td><td "
                             "class=\"tdname\"><a href=\"/product/jLF48d/amd-ryzen-5-2600-34ghz-6-core-processor-yd2600"
                             "bbafbox\">AMD Ryzen 5 2600</a></td><td style=\"text-align:right;\">3.4 GHz</td><td style="
                             "\"text-align:center;\">6</td><td style=\"text-align:right;\">65 W</td><td class=\"inline-"
                             "rating-sm\" data-ci=\"967\"><div class=\"rating\"><ul class=\"stars\"><li class=\"full-st"
                             "ar\"></li><li class=\"full-star\"></li><li class=\"full-star\"></li><li class=\"full-star"
                             "\"></li><li class=\"half-star\"></li></ul></div> (104)</td><td class=\"tdprice\">$164.99<"
                             "/td><td class=\"viewadd\"><a href=\"#jLF48d\" class=\"btn-mds pp_add_part\">Add</a></td><"
                             "/tr>"}])


def test_parser_default_region():
    parser = Parser()
    assert parser._region == "us"
    assert parser._currency_sign == "$"
    assert parser._currency == USD


def test_parser_set_region_in():
    parser = Parser()
    parser._set_region("in")
    assert parser._region == "in"
    assert parser._currency_sign == "₹"
    assert parser._currency == INR


def test_parser_set_region_se():
    parser = Parser()
    parser._set_region("se")
    assert parser._region == "se"
    assert parser._currency_sign == "kr"
    assert parser._currency == SEK


def test_parser_set_region_be():
    parser = Parser()
    parser._set_region("be")
    assert parser._region == "be"
    assert parser._currency_sign == "€"
    assert parser._currency == EUR


def test_parser_set_region_uk():
    parser = Parser()
    parser._set_region("uk")
    assert parser._region == "uk"
    assert parser._currency_sign == "£"
    assert parser._currency == GBP