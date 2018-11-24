import pytest
import asyncio
from pcpartpicker.parser import Parser, Result
from pcpartpicker.scraper import Scraper
from pcpartpicker.parts import *
from moneyed import Money, USD


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


def test_parser_parse():
    parts = {"cpu": CPU, "case": Case, "headphones": Headphones}
    scraper = Scraper()
    parser = Parser()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(scraper._retrieve(loop, *parts.keys()))
    loop.close()
    for args in zip(parts.keys(), results):
        parsed_result = parser._parse(args)
        returned_part, parsed_data = parsed_result
        assert returned_part == args[0]
        for item in parsed_data:
            if not item or not isinstance(item, parts.get(args[0])):
                raise AssertionError


def test_parser_retrieve_data_well_formed():
    parser = Parser()
    raw_data = ["this", "is" "a" "test", "Add", "there", "should", "be", "two", "chunked",
                "segments", "Add"]
    chunked_data = list(parser._retrieve_data(raw_data))
    assert len(chunked_data) == 2


def test_parser_retrieve_data_poorly_formed():
    parser = Parser()
    raw_data = ["this", "is" "a" "test", "Add", "there", "should", "be", "two", "chunked",
                "segments", "Add", "This", "should", "not", "be", "considered", "valid"]
    chunked_data = list(parser._retrieve_data(raw_data))
    assert len(chunked_data) == 2


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
    assert result.clock_speed == ClockSpeed.from_GHz(3.4)
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


def test_parser_retrieve_int_well_formed():
    parser = Parser()
    result = parser._retrieve_int("2")
    assert isinstance(result, Result)
    assert result.iterate == 1
    assert not result.tuple
    assert result.value == 2


def test_parser_retrieve_int_poorly_formed():
    parser = Parser()
    with pytest.raises(ValueError) as excinfo:
        result = parser._retrieve_int("2.3")
        assert "Not a valid int string!" in excinfo.value
    with pytest.raises(ValueError) as excinfo:
        result = parser._retrieve_int(" 500 W")
        assert "Not a valid int string!" in excinfo.value


def test_parser_retrieve_int_none():
    parser = Parser()
    result = parser._retrieve_int(None)
    assert isinstance(result, Result)
    assert not result.value
    assert result.iterate == 0
    assert not result.tuple


def test_parser_retrieve_float():
    pass
