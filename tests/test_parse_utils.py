import unittest

from pcpartpicker.parse_utils import tokenize, num, boolean, core_clock, decibels, default, fan_cfm, fan_rpm, \
    frequency_response, grams, hdd_data, memory_sizes, memory_type, network_speed, price, resolution, retrieve_float, \
    retrieve_int, to_bytes, wr_speeds, wattage, va
from pcpartpicker.parts import Bytes, CFM, ClockSpeed, Decibels, FrequencyResponse, NetworkSpeed, Resolution, RPM


class ParseUtilsTest(unittest.TestCase):

    def test_tokenize_cpu(self):
        raw_data = ["AMD Ryzen 2600", "3.4 GHz", "6", "65 W", "$164.99", "Intel Core i7-8700K", "3.7 GHz", "6", "95 W",
                    "$369.99"]
        cpu1 = ["AMD Ryzen 2600", "3.4 GHz", "6", "65 W", "$164.99"]
        cpu2 = ["Intel Core i7-8700K", "3.7 GHz", "6", "95 W", "$369.99"]
        data_chunks = list(tokenize("cpu", raw_data))
        self.assertEqual(len(data_chunks), 2)
        self.assertEqual(data_chunks[0], cpu1)
        self.assertEqual(len(data_chunks[0]), 5)
        self.assertEqual(data_chunks[1], cpu2)
        self.assertEqual(len(data_chunks[1]), 5)

    def test_num_int(self):
        data = "$34"
        self.assertEqual(num(data), 34)

    def test_num_float(self):
        data = "$34.45"
        self.assertEqual(num(data), 34.45)

    def test_boolean_yes(self):
        data = "Yes"
        self.assertTrue(boolean(data))

    def test_boolean_no(self):
        data = "No"
        self.assertFalse(boolean(data))

    def test_core_clock_mhz(self):
        clock = "3.45 MHz"
        self.assertEqual(core_clock(clock), ClockSpeed.from_mhz(3.45))

    def test_core_clock_ghz(self):
        clock = "3.45 GHz"
        self.assertEqual(core_clock(clock), ClockSpeed.from_ghz(3.45))

    def test_core_clock_invalid(self):
        clock = "$3.45"
        self.assertIsNone(core_clock(clock))

    def test_decibels_range(self):
        decibel_info = "9 dB - 36 dB"
        self.assertEqual(decibels(decibel_info), Decibels(9, 36, None))

    def test_decibels_average(self):
        decibel_info = "34 dB"
        self.assertEqual(decibels(decibel_info), Decibels(None, None, 34))

    def test_default(self):
        self.assertEqual(default("default"), "default")

    def test_fan_cfm_range(self):
        cfm_info = "12 CFM - 75 CFM"
        self.assertEqual(fan_cfm(cfm_info), CFM(12, 75, None))

    def test_fan_cfm_average(self):
        cfm_info = "75 CFM"
        self.assertEqual(fan_cfm(cfm_info), CFM(None, None, 75))

    def test_fan_cfm_none(self):
        cfm_info = "CFM"
        self.assertIsNone(fan_cfm(cfm_info))

    def test_fan_rpm_range(self):
        rpm_info = "600 - 1500 RPM"
        self.assertEqual(fan_rpm(rpm_info), RPM(600, 1500, None))

    def test_fan_rpm_average(self):
        rpm_info = "1500 RPM"
        self.assertEqual(fan_rpm(rpm_info), RPM(None, None, 1500))

    def test_fan_rpm_none(self):
        rpm_info = "RPM"
        self.assertIsNone(fan_rpm(rpm_info))

    def test_freq_response_range(self):
        freq_info = "15 Hz - 25 Hz"
        self.assertEqual(frequency_response(freq_info), FrequencyResponse(15.0, 25.0, None))

    def test_freq_response_range_khz(self):
        freq_info = "15 kHz - 25 kHz"
        self.assertEqual(frequency_response(freq_info), FrequencyResponse(15000.0, 25000.0, None))

    def test_grams_g(self):
        gram_info = "34 g"
        self.assertEqual(grams(gram_info), 34)

    def test_grams_mg(self):
        gram_info = "34 mg"
        self.assertEqual(grams(gram_info), .034)

    def test_hdd_data_hdd(self):
        hdd_info = "7200 RPM"
        self.assertEqual(hdd_data(hdd_info), ("HDD", 7200))

    def test_hdd_data_ssd(self):
        hdd_info = "SSD"
        self.assertEqual(hdd_data(hdd_info), ("SSD", None))

    def test_hdd_data_hybrid(self):
        hdd_info = "Hybrid"
        self.assertEqual(hdd_data(hdd_info), ("Hybrid", None))

    def test_memory_sizes_two_modules_eight_gb(self):
        mem_info = "2x8 GB"
        self.assertEqual(memory_sizes(mem_info), (2, Bytes.from_gb(8)))

    def test_memory_sizes_one_module_eight_gb(self):
        mem_info = "1x8 GB"
        self.assertEqual(memory_sizes(mem_info), (1, Bytes.from_gb(8)))

    def test_memory_type_ddr4_3000(self):
        mem_info = "DDR4-3000"
        self.assertEqual(memory_type(mem_info), ("DDR4", ClockSpeed.from_mhz(3000)))

    def test_memory_type_ddr3_2000(self):
        mem_info = "DDR3-2000"
        self.assertEqual(memory_type(mem_info), ("DDR3", ClockSpeed.from_mhz(2000)))

    def test_network_speed_1000_mbits_1_port(self):
        net_info = "1000 Mbit/s"
        self.assertEqual(network_speed(net_info), (NetworkSpeed.from_mbits(1000), 1))

    def test_network_speed_2_gbits_1_port(self):
        net_info = "2 Gbit/s"
        self.assertEqual(network_speed(net_info), (NetworkSpeed.from_gbits(2), 1))

    def test_network_speed_1000_mbits_2_ports(self):
        net_info = "1000 Mbit/s x 2"
        self.assertEqual(network_speed(net_info), (NetworkSpeed.from_mbits(1000), 2))

    def test_network_speed_2_gbits_4_ports(self):
        net_info = "2 Gbit/s x 4"
        self.assertEqual(network_speed(net_info), (NetworkSpeed.from_gbits(2), 4))

    def test_price(self):
        price_info = "$34"
        self.assertEqual(price(price_info), "$34")

    def test_resolution(self):
        res_info = "2560 x 1440"
        self.assertEqual(resolution(res_info), Resolution(2560, 1440))

    def test_retrieve_float(self):
        float_info = "dollars 234.00 dollars"
        self.assertEqual(retrieve_float(float_info), 234.00)

    def test_retrieve_int(self):
        int_info = "dollars 234 dollars"
        self.assertEqual(retrieve_int(int_info), 234)

    def test_to_bytes_kb(self):
        byte_info = "3.4 KB"
        self.assertEqual(to_bytes(byte_info), Bytes.from_kb(3.4))

    def test_to_bytes_mb(self):
        byte_info = "3.4 MB"
        self.assertEqual(to_bytes(byte_info), Bytes.from_mb(3.4))

    def test_to_bytes_gb(self):
        byte_info = "3.4 GB"
        self.assertEqual(to_bytes(byte_info), Bytes.from_gb(3.4))

    def test_to_bytes_tb(self):
        byte_info = "3.4 TB"
        self.assertEqual(to_bytes(byte_info), Bytes.from_tb(3.4))

    def test_to_bytes_pb(self):
        byte_info = "3.4 PB"
        self.assertEqual(to_bytes(byte_info), Bytes.from_pb(3.4))

    def test_to_bytes_none(self):
        byte_info = "3.4"
        self.assertIsNone(to_bytes(byte_info))

    def test_wr_speeds_default(self):
        wr_info = "14/12/2/2"
        self.assertEqual(wr_speeds(wr_info), "14/12/2/2")

    def test_wr_speeds_none(self):
        wr_info = "-/-/-/-"
        self.assertIsNone(wr_speeds(wr_info))

    def test_wattage_int_kw(self):
        watt_info = "1000 kW"
        self.assertEqual(wattage(watt_info), 1000000)

    def test_wattage_int_w(self):
        watt_info = "1000 W"
        self.assertEqual(wattage(watt_info), 1000)

    def test_wattage_float_kw(self):
        watt_info = "1.3 kW"
        self.assertEqual(wattage(watt_info), 1300)

    def test_va_va(self):
        va_info = "100 VA"
        self.assertEqual(va(va_info), 100.0)

    def test_va_kva(self):
        va_info = "1.34 kVA"
        self.assertEqual(va(va_info), 1340)
