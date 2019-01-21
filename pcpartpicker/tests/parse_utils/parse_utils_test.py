import pytest

from ...parse_utils import tokenize, num, boolean, core_clock, decibels, default, fan_cfm, fan_rpm, \
    frequency_response, grams, hdd_data, memory_sizes, memory_type, network_speed, price, resolution, retrieve_float, \
    retrieve_int, to_bytes, wr_speeds, wattage, va
from ...parts import Bytes, CFM, ClockSpeed, Decibels, FrequencyResponse, NetworkSpeed, Resolution, RPM


def test_tokenize_cpu():
    raw_data = ["AMD Ryzen 2600", "3.4 GHz", "6", "65 W", "$164.99", "Intel Core i7-8700K", "3.7 GHz", "6", "95 W",
                "$369.99"]
    cpu1 = ["AMD Ryzen 2600", "3.4 GHz", "6", "65 W", "$164.99"]
    cpu2 = ["Intel Core i7-8700K", "3.7 GHz", "6", "95 W", "$369.99"]
    data_chunks = list(tokenize("cpu", raw_data))
    assert len(data_chunks) == 2
    assert data_chunks[0] == cpu1
    assert len(data_chunks[0]) == 5
    assert data_chunks[1] == cpu2
    assert len(data_chunks[1]) == 5


def test_num_int():
    data = "$34"
    assert num(data) == 34


def test_num_float():
    data = "$34.45"
    assert num(data) == 34.45


def test_boolean_yes():
    data = "Yes"
    assert boolean(data)


def test_boolean_no():
    data = "No"
    assert not boolean(data)


def test_boolean_invalid():
    data = "#$2"
    with pytest.raises(ValueError):
        boolean(data)


def test_core_clock_mhz():
    clock = "3.45 MHz"
    assert core_clock(clock) == ClockSpeed.from_MHz(3.45)


def test_core_clock_ghz():
    clock = "3.45 GHz"
    assert core_clock(clock) == ClockSpeed.from_GHz(3.45)


def test_core_clock_invalid():
    clock = "$3.45"
    assert not core_clock(clock)


def test_decibels_range():
    decibel_info = "9 dB - 36 dB"
    assert decibels(decibel_info) == Decibels(9, 36, None)


def test_decibels_average():
    decibel_info = "34 dB"
    assert decibels(decibel_info) == Decibels(None, None, 34)


def test_default():
    assert default("default") == "default"


def test_fan_cfm_range():
    cfm_info = "12 CFM - 75 CFM"
    assert fan_cfm(cfm_info) == CFM(12, 75, None)


def test_fan_cfm_average():
    cfm_info = "75 CFM"
    assert fan_cfm(cfm_info) == CFM(None, None, 75)


def test_fan_cfm_none():
    cfm_info = "CFM"
    assert not fan_cfm(cfm_info)


def test_fan_rpm_range():
    rpm_info = "600 - 1500 RPM"
    assert fan_rpm(rpm_info) == RPM(600, 1500, None)


def test_fan_rpm_average():
    rpm_info = "1500 RPM"
    assert fan_rpm(rpm_info) == RPM(None, None, 1500)


def test_fan_rpm_none():
    rpm_info = "RPM"
    assert not fan_rpm(rpm_info)


def test_freq_response_range():
    freq_info = "15 Hz - 25 Hz"
    assert frequency_response(freq_info) == FrequencyResponse(15.0, 25.0, None)


def test_freq_response_range_khz():
    freq_info = "15 kHz - 25 kHz"
    assert frequency_response(freq_info) == FrequencyResponse(15000.0, 25000.0, None)


def test_grams_g():
    gram_info = "34 g"
    assert grams(gram_info) == 34


def test_grams_mg():
    gram_info = "34 mg"
    assert grams(gram_info) == .034


def test_hdd_data_hdd():
    hdd_info = "7200 RPM"
    assert hdd_data(hdd_info) == ("HDD", 7200)


def test_hdd_data_ssd():
    hdd_info = "SSD"
    assert hdd_data(hdd_info) == ("SSD", None)


def test_hdd_data_hybrid():
    hdd_info = "Hybrid"
    assert hdd_data(hdd_info) == ("Hybrid", None)


def test_memory_sizes_two_modules_eight_gb():
    mem_info = "2x8 GB"
    assert memory_sizes(mem_info) == (2, Bytes.from_GB(8))


def test_memory_sizes_one_module_eight_gb():
    mem_info = "1x8 GB"
    assert memory_sizes(mem_info) == (1, Bytes.from_GB(8))


def test_memory_type_ddr4_3000():
    mem_info = "DDR4-3000"
    assert memory_type(mem_info) == ("DDR4", ClockSpeed.from_MHz(3000))


def test_memory_type_ddr3_2000():
    mem_info = "DDR3-2000"
    assert memory_type(mem_info) == ("DDR3", ClockSpeed.from_MHz(2000))


def test_network_speed_1000_mbits_1_port():
    net_info = "1000 Mbit/s"
    assert network_speed(net_info) == (NetworkSpeed.from_Mbits(1000), 1)


def test_network_speed_2_gbits_1_port():
    net_info = "2 Gbit/s"
    assert network_speed(net_info) == (NetworkSpeed.from_Gbits(2), 1)


def test_network_speed_1000_mbits_2_ports():
    net_info = "1000 Mbit/s x 2"
    assert network_speed(net_info) == (NetworkSpeed.from_Mbits(1000), 2)


def test_network_speed_2_gbits_4_ports():
    net_info = "2 Gbit/s x 4"
    assert network_speed(net_info) == (NetworkSpeed.from_Gbits(2), 4)


def test_price():
    price_info = "$34"
    assert price(price_info) == "$34"


def test_resolution():
    res_info = "2560 x 1440"
    assert resolution(res_info) == Resolution(2560, 1440)


def test_retrieve_float():
    float_info = "dollars 234.00 dollars"
    assert retrieve_float(float_info) == 234.00


def test_retrieve_int():
    int_info = "dollars 234 dollars"
    assert retrieve_int(int_info) == 234


def test_to_bytes_kb():
    byte_info = "3.4 KB"
    assert to_bytes(byte_info) == Bytes.from_KB(3.4)


def test_to_bytes_mb():
    byte_info = "3.4 MB"
    assert to_bytes(byte_info) == Bytes.from_MB(3.4)


def test_to_bytes_gb():
    byte_info = "3.4 GB"
    assert to_bytes(byte_info) == Bytes.from_GB(3.4)


def test_to_bytes_tb():
    byte_info = "3.4 TB"
    assert to_bytes(byte_info) == Bytes.from_TB(3.4)


def test_to_bytes_pb():
    byte_info = "3.4 PB"
    assert to_bytes(byte_info) == Bytes.from_PB(3.4)


def test_to_bytes_none():
    byte_info = "3.4"
    assert not to_bytes(byte_info)


def test_wr_speeds_default():
    wr_info = "14/12/2/2"
    assert wr_speeds(wr_info) == "14/12/2/2"


def test_wr_speeds_none():
    wr_info = "-/-/-/-"
    assert not wr_speeds(wr_info)


def test_wattage_int_kw():
    watt_info = "1000 kW"
    assert wattage(watt_info) == 1000000


def test_wattage_int_w():
    watt_info = "1000 W"
    assert wattage(watt_info) == 1000


def test_wattage_float_kw():
    watt_info = "1.3 kW"
    assert wattage(watt_info) == 1300


def test_wattage_float_w():
    watt_info = "13.45 W"
    assert wattage(watt_info) == 13.45


def test_va_va():
    va_info = "100 VA"
    assert va(va_info) == 100.0


def test_va_kva():
    va_info = "1.34 kVA"
    assert va(va_info) == 1340
