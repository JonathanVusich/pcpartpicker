import pytest
from pcpartpicker.parser import Parser


def test_parser_default_region():
    parser = Parser()
    assert parser._region == "us"
    assert parser._currency_sign == "$"


def test_parser_set_region_in():
    parser = Parser()
    parser._set_region("in")
    assert parser._region == "in"
    assert parser._currency_sign == "₹"


def test_parser_set_region_se():
    parser = Parser()
    parser._set_region("se")
    assert parser._region == "se"
    assert parser._currency_sign == "kr"


def test_parser_set_region_be():
    parser = Parser()
    parser._set_region("be")
    assert parser._region == "be"
    assert parser._currency_sign == "€"


def test_parser_set_region_uk():
    parser = Parser()
    parser._set_region("uk")
    assert parser._region == "uk"
    assert parser._currency_sign == "£"


