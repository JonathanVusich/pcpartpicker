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


def test_parser_parse_function(raw_html):
    parser = Parser()
    parsed_result = parser._parse(raw_html)
    returned_part, parsed_data = parsed_result
    assert returned_part == raw_html[0]
    assert len(parsed_data) == 1
    assert isinstance(parsed_data[0], CPU)


def test_parser_parse_token_no_information():
    raw_data = ["$99.00"]
    parser = Parser()
    result = parser._parse_token("cpu", raw_data)
    assert not result


def test_parser_parse_token_cpu_well_formed():
    raw_data = ["Intel Core i7", "3.4 GHz", "8", "220 W", "$99.00"]
    parser = Parser()
    result = parser._parse_token("cpu", raw_data)
    assert isinstance(result, CPU)
    assert result.model == "Intel Core i7"
    assert result.clock_speed == ClockSpeed.from_ghz(3.4)
    assert result.cores == 8
    assert result.tdp == 220
    assert result.price == Money("99.00", USD)


def test_parser_parse_token_cpu_only_name():
    raw_data = ["Intel Core i7"]
    parser = Parser()
    result = parser._parse_token("cpu", raw_data)
    assert isinstance(result, CPU)
    assert result.model == "Intel Core i7"
    assert not result.clock_speed
    assert not result.cores
    assert not result.tdp
    assert result.price == Money("0.00", USD)


def test_parser_parse_token_cpu_no_clock_speed():
    raw_data = ["Intel Core i7", "8", "220 W", "$99.00"]
    parser = Parser()
    result = parser._parse_token("cpu", raw_data)
    assert isinstance(result, CPU)
    assert result.model == "Intel Core i7"
    assert not result.clock_speed
    assert result.cores == 8
    assert result.tdp == 220
    assert result.price == Money("99.00", USD)


def test_parser_parse_token_cpu_no_clock_speed_or_cores():
    raw_data = ["Intel Core i7", "220 W", "$99.00"]
    parser = Parser()
    result = parser._parse_token("cpu", raw_data)
    assert isinstance(result, CPU)
    assert result.model == "Intel Core i7"
    assert not result.clock_speed
    assert not result.cores
    assert result.tdp == 220
    assert result.price == Money("99.00", USD)


def test_parser_parse_token_cpu_no_cs_cores_or_tdp():
    raw_data = ["Intel Core i7", "$99.00"]
    parser = Parser()
    result = parser._parse_token("cpu", raw_data)
    assert isinstance(result, CPU)
    assert result.model == "Intel Core i7"
    assert not result.clock_speed
    assert not result.cores
    assert not result.tdp
    assert result.price == Money("99.00", USD)


def test_parser_parse_toke_cpu_cooler_well_formed():
    raw_data = ["CoolerMaster Hyper 212 Evo", "600 - 2000 RPM", "9.3 dB - 36 dB", "$99.00"]
    parser = Parser()
    result = parser._parse_token("cpu-cooler", raw_data)
    assert isinstance(result, CPUCooler)
    assert result.model == "CoolerMaster Hyper 212 Evo"
    assert result.fan_rpm == RPM(600, 2000, None)
    assert result.decibels == Decibels(9.3, 36.0, None)
    assert result.price == Money("99.00", USD)


def test_parser_parse_toke_cpu_cooler_no_rpm():
    raw_data = ["CoolerMaster Hyper 212 Evo", "-", "9.3 dB - 36 dB", "$99.00"]
    parser = Parser()
    result = parser._parse_token("cpu-cooler", raw_data)
    assert isinstance(result, CPUCooler)
    assert result.model == "CoolerMaster Hyper 212 Evo"
    assert not result.fan_rpm
    assert result.decibels == Decibels(9.3, 36.0, None)
    assert result.price == Money("99.00", USD)


def test_parser_parse_toke_cpu_cooler_no_rpm_or_decibels():
    raw_data = ["CoolerMaster Hyper 212 Evo", "-", "$99.00"]
    parser = Parser()
    result = parser._parse_token("cpu-cooler", raw_data)
    assert isinstance(result, CPUCooler)
    assert result.model == "CoolerMaster Hyper 212 Evo"
    assert not result.fan_rpm
    assert not result.decibels
    assert result.price == Money("99.00", USD)


def test_parser_parse_token_cpu_cooler_only_model():
    raw_data = ["CoolerMaster Hyper 212 Evo"]
    parser = Parser()
    result = parser._parse_token("cpu-cooler", raw_data)
    assert isinstance(result, CPUCooler)
    assert result.model == "CoolerMaster Hyper 212 Evo"
    assert not result.fan_rpm
    assert not result.decibels
    assert result.price == Money("0.00", USD)

