import unittest

from moneyed import Money, USD

from pcpartpicker.parts import *


class PartTest(unittest.TestCase):

    def test_check_typing(self):
        self.assertIsNone(check_typing(12, int))
        with self.assertRaises(ValueError):
            check_typing(12.3, int)
        self.assertIsNone(check_typing(None, int))

    def test_bytes_init(self):
        size = Bytes(50)
        self.assertEquals(size.total, 50)
        self.assertEquals(size.kb, 0.05)
        self.assertEquals(size.mb, 0.00005)
        self.assertEquals(size.gb, 0.00000005)
        self.assertEquals(size.tb, 0.00000000005)
        self.assertEquals(size.pb, 0.00000000000005)

    def test_bytes_bad_init(self):
        with self.assertRaises(ValueError):
            _ = Bytes("50")

    def test_bytes_from_kb(self):
        size = Bytes.from_kb(50)
        self.assertEqual(size.total, 50000)
        self.assertEqual(size.kb, 50)
        self.assertEqual(size.mb, 0.05)
        self.assertEqual(size.gb, 0.00005)
        self.assertEqual(size.tb, 0.00000005)
        self.assertEqual(size.pb, 0.00000000005)

    def test_bytes_from_mb(self):
        size = Bytes.from_mb(50)
        self.assertEqual(size.total, 50000000)
        self.assertEqual(size.kb, 50000)
        self.assertEqual(size.mb, 50)
        self.assertEqual(size.gb, 0.05)
        self.assertEqual(size.tb, 0.00005)
        self.assertEqual(size.pb, 0.00000005)

    def test_bytes_from_gb(self):
        size = Bytes.from_gb(50)
        self.assertEqual(size.total, 50000000000)
        self.assertEqual(size.kb, 50000000)
        self.assertEqual(size.mb, 50000)
        self.assertEqual(size.gb, 50)
        self.assertEqual(size.tb, 0.05)
        self.assertEqual(size.pb, 0.00005)

    def test_bytes_from_tb(self):
        size = Bytes.from_tb(50)
        self.assertEqual(size.total, 50000000000000)
        self.assertEqual(size.kb, 50000000000)
        self.assertEqual(size.mb, 50000000)
        self.assertEqual(size.gb, 50000)
        self.assertEqual(size.tb, 50)
        self.assertEqual(size.pb, 0.05)

    def test_bytes_from_pb(self):
        size = Bytes.from_pb(50)
        self.assertEqual(size.total, 50000000000000000)
        self.assertEqual(size.kb, 50000000000000)
        self.assertEqual(size.mb, 50000000000)
        self.assertEqual(size.gb, 50000000)
        self.assertEqual(size.tb, 50000)
        self.assertEqual(size.pb, 50)

    def test_resolution_init(self):
        resolution = Resolution(1920, 1080)
        self.assertEqual(resolution.width, 1920)
        self.assertEqual(resolution.height, 1080)

    def test_resolution_bad_init(self):
        with self.assertRaises(ValueError):
            _ = Resolution("1920", "1080")

    def test_clock_speed_init(self):
        clock_speed = ClockSpeed(3450000000)
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)

    def test_clock_speed_bad_init(self):
        with self.assertRaises(ValueError):
            _ = ClockSpeed("This is a test")

    def test_clock_speed_from_GHz_float(self):
        clock_speed = ClockSpeed.from_ghz(3.45)
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)
        self.assertEqual(clock_speed.cycles, 3450000000)

    def test_clock_speed_from_GHz_str(self):
        clock_speed = ClockSpeed.from_ghz("3.45")
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)
        self.assertEqual(clock_speed.cycles, 3450000000)

    def test_clock_speed_from_GHz_bad_str(self):
        with self.assertRaises(ValueError):
            _ = ClockSpeed.from_ghz("This is a test")

    def test_clock_speed_from_MHz_float(self):
        clock_speed = ClockSpeed.from_mhz(3450)
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)
        self.assertEqual(clock_speed.cycles, 3450000000)

    def test_clock_speed_from_MHz_str(self):
        clock_speed = ClockSpeed.from_mhz("3450")
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)
        self.assertEqual(clock_speed.cycles, 3450000000)

    def test_clock_speed_from_MHz_bad_str(self):
        with self.assertRaises(ValueError):
            _ = ClockSpeed.from_mhz("this is a test")

    def test_decibel_init(self):
        decibels = Decibels(12.5, 34.5, 22)
        self.assertEqual(decibels.min, 12.5)
        self.assertEqual(decibels.max, 34.5)
        self.assertEqual(decibels.default, 22)

    def test_decibel_bad_init(self):
        with self.assertRaises(ValueError):
            args = ["12.5", "34.5", "23.1"]
            _ = Decibels(*args)

    def test_rpm_init(self):
        args = [12.5, 34.5, 22]
        rpm = RPM(*args)
        self.assertEqual(rpm.min, args[0])
        self.assertEqual(rpm.max, args[1])
        self.assertEqual(rpm.default, args[2])

    def test_rpm_bad_init(self):
        with self.assertRaises(ValueError):
            args = ["12.5", "34.5", "23.1"]
            _ = RPM(*args)

    def test_cfm_init(self):
        args = [12.5, 34.5, 22]
        cfm = CFM(*args)
        self.assertEqual(cfm.min, args[0])
        self.assertEqual(cfm.max, args[1])
        self.assertEqual(cfm.default, args[2])

    def test_cfm_bad_init(self):
        args = ["12.5", "34.5", "23.1"]
        with self.assertRaises(ValueError):
            _ = CFM(*args)

    def test_network_speed_init(self):
        network_speed = NetworkSpeed(2000)
        self.assertEqual(network_speed.bits_per_second, 2000)

    def test_network_speed_bad_init(self):
        with self.assertRaises(ValueError):
            _ = NetworkSpeed.from_gbits("2")

    def test_network_speed_from_mbits(self):
        network_speed = NetworkSpeed.from_mbits(1000)
        self.assertEqual(network_speed.mbits, 1000)
        self.assertEqual(network_speed.gbits, 1)

    def test_network_speed_from_gbits(self):
        network_speed = NetworkSpeed.from_gbits(2)
        self.assertEqual(network_speed.mbits, 2000)
        self.assertEqual(network_speed.gbits, 2)

    def test_cpu_init(self):
        args = ["Intel Core i7-6700k", ClockSpeed.from_ghz(4.4), 4, 95, Money("230.00", USD)]
        cpu = CPU(*args)
        self.assertEqual(cpu.model, args[0])
        self.assertEqual(cpu.clock_speed, args[1])
        self.assertEqual(cpu.cores, args[2])
        self.assertEqual(cpu.tdp, args[3])
        self.assertEqual(cpu.price, args[4])

    def test_cpu_bad_init(self):
        args = [6700, ClockSpeed.from_ghz("4.4"), 4, 95, Money("230.00", USD)]
        with self.assertRaises(ValueError):
            _ = CPU(*args)

    def test_cpu_cooler_init(self):
        args = ["Cooler Master Hyper 212 Evo", RPM(500, 2400, 1800), Decibels(12.2, 43.8, 30.2), Money("25.99", USD)]
        cpu_cooler = CPUCooler(*args)
        self.assertEqual(cpu_cooler.model, args[0])
        self.assertEqual(cpu_cooler.fan_rpm, args[1])
        self.assertEqual(cpu_cooler.decibels, args[2])
        self.assertEqual(cpu_cooler.price, args[3])

    def test_cpu_cooler_bad_init(self):
        args = ["Cooler Master Hyper 212 Evo", 5000, Decibels(12.2, 43.8, 30.2), Money("25.99", USD)]
        with self.assertRaises(ValueError):
            _ = CPUCooler(*args)

    def test_motherboard_init(self):
        args = ["MSI Z170", "Z170", "ATX", 2, Bytes.from_gb(8), Money("89.11", USD)]
        mobo = Motherboard(*args)
        self.assertEqual(mobo.model, args[0])
        self.assertEqual(mobo.socket, args[1])
        self.assertEqual(mobo.form_factor, args[2])
        self.assertEqual(mobo.ram_slots, args[3])
        self.assertEqual(mobo.max_ram, args[4])
        self.assertEqual(mobo.price, args[5])

    def test_motherboard_bad_init(self):
        args = ["MSI Z170", "Z170", "ATX", "2", Bytes.from_gb(8), Money("89.11", USD)]
        with self.assertRaises(ValueError):
            _ = Motherboard(*args)

    def test_memory_init(self):
        args = ["Corsair Vengeance", "DDR4", ClockSpeed.from_mhz("3000"), "288-pin DIMM", 15,
                2, Bytes.from_gb(8), Bytes.from_gb(16), Money("0.22", USD), Money("122.45", USD)]
        memory = Memory(*args)
        self.assertEqual(memory.model, args[0])
        self.assertEqual(memory.module_type, args[1])
        self.assertEqual(memory.speed, args[2])
        self.assertEqual(memory.form_factor, args[3])
        self.assertEqual(memory.cas_timing, args[4])
        self.assertEqual(memory.number_of_modules, args[5])
        self.assertEqual(memory.module_size, args[6])
        self.assertEqual(memory.total_size, args[7])
        self.assertEqual(memory.price_per_gb, args[8])
        self.assertEqual(memory.price, args[9])

    def test_memory_bad_init(self):
        args = ["Corsair Vengeance", "DDR4", ClockSpeed.from_mhz("3000"), "288-pin DIMM", 15,
                2, Bytes.from_gb(8), Bytes.from_gb(16), 0.22, Money("122.45", USD)]
        with self.assertRaises(ValueError):
            _ = Memory(*args)

    def test_storage_drive_init(self):
        args = ["Seagate", "WD Black", "2.5 in", "HDD", None, Bytes.from_tb(4), Bytes.from_mb(256), Money("0.08", USD),
                Money("123.00", USD)]
        hdd = StorageDrive(*args)
        self.assertEqual(hdd.model, args[0])
        self.assertEqual(hdd.model_line, args[1])
        self.assertEqual(hdd.form_factor, args[2])
        self.assertEqual(hdd.type, args[3])
        self.assertEqual(hdd.platter_rpm, args[4])
        self.assertEqual(hdd.capacity, args[5])
        self.assertEqual(hdd.cache_amount, args[6])
        self.assertEqual(hdd.price_per_gb, args[7])
        self.assertEqual(hdd.price, args[8])

    def test_storage_drive_bad_init(self):
        args = ["Seagate", "WD Black", "2.5 in", 7200, None, Bytes.from_tb(4), Bytes.from_mb(256), Money("0.08", USD),
                Money("123.00", USD)]
        with self.assertRaises(ValueError):
            _ = StorageDrive(*args)

    def test_gpu_init(self):
        args = ["EVGA", "RTX 2080", "T104", Bytes.from_gb(8), ClockSpeed.from_ghz(2), Money("300.00", USD)]
        gpu = GPU(*args)
        self.assertEqual(gpu.model, args[0])
        self.assertEqual(gpu.model_line, args[1])
        self.assertEqual(gpu.chipset, args[2])
        self.assertEqual(gpu.memory_amount, args[3])
        self.assertEqual(gpu.core_clock, args[4])
        self.assertEqual(gpu.price, args[5])

    def test_gpu_bad_init(self):
        args = ["EVGA", "RTX 2080", 104, Bytes.from_gb(8), ClockSpeed.from_ghz(2), Money("300.00", USD)]
        with self.assertRaises(ValueError):
            _ = GPU(*args)

    def test_psu_init(self):
        args = ["EVGA", "G1", "ATX", "80+ Gold", 800, "Fully modular", Money("120", USD)]
        psu = PSU(*args)
        self.assertEqual(psu.model, args[0])
        self.assertEqual(psu.model_line, args[1])
        self.assertEqual(psu.form_factor, args[2])
        self.assertEqual(psu.efficiency_rating, args[3])
        self.assertEqual(psu.watt_rating, args[4])
        self.assertEqual(psu.modular, args[5])
        self.assertEqual(psu.price, args[6])

    def test_psu_bad_init(self):
        args = ["EVGA", "G1", "ATX", 80, 800, "Fully modular", Money("120", USD)]
        with self.assertRaises(ValueError):
            _ = PSU(*args)

    def test_case_init(self):
        args = ["Lian Li", "ATX", 4, 4, None, Money("120", USD)]
        case = Case(*args)
        self.assertEqual(case.model, args[0])
        self.assertEqual(case.form_factor, args[1])
        self.assertEqual(case.external_bays, args[2])
        self.assertEqual(case.internal_bays, args[3])
        self.assertEqual(case.psu_wattage, args[4])

    def test_case_bad_init(self):
        args = ["Lian Li", "ATX", 4, 4, "435", Money("120", USD)]
        with self.assertRaises(ValueError):
            _ = Case(*args)

    def test_fan_init(self):
        args = ["Cooler Master", "black", 120, RPM(800, 2500, 1800), CFM(4, 21, 16), Decibels(21, 45, 33),
                Money("23.34", USD)]
        fan = Fan(*args)
        self.assertEqual(fan.model, args[0])
        self.assertEqual(fan.color, args[1])
        self.assertEqual(fan.size, args[2])
        self.assertEqual(fan.rpm, args[3])
        self.assertEqual(fan.airflow, args[4])
        self.assertEqual(fan.decibels, args[5])
        self.assertEqual(fan.price, args[6])

    def test_fan_bad_init(self):
        args = ["Cooler Master", True, 120, RPM(800, 2500, 1800), CFM(4, 21, 16), Decibels(21, 45, 33),
                Money("23.34", USD)]
        with self.assertRaises(ValueError):
            _ = Fan(*args)

    def test_fan_controller_init(self):
        args = ["Cooler Master", "5.25\'", 5, 12, Money("60.00", USD)]
        fan_controller = FanController(*args)
        self.assertEqual(fan_controller.model, args[0])
        self.assertEqual(fan_controller.form_factor, args[1])
        self.assertEqual(fan_controller.channels, args[2])
        self.assertEqual(fan_controller.channel_wattage, args[3])
        self.assertEqual(fan_controller.price, args[4])

    def test_fan_controller_bad_init(self):
        args = ["Cooler Master", "5.25\'", 5, "12", Money("60.00", USD)]
        with self.assertRaises(ValueError):
            _ = FanController(*args)

    def test_thermal_paste_init(self):
        args = ["Cooler Master", 23, Money("23.45", USD)]
        thermal_paste = ThermalPaste(*args)
        self.assertEqual(thermal_paste.model, args[0])
        self.assertEqual(thermal_paste.amount, args[1])
        self.assertEqual(thermal_paste.price, args[2])

    def test_thermal_paste_bad_init(self):
        args = ["Cooler Master", "23", Money("23.45", USD)]
        with self.assertRaises(ValueError):
            _ = ThermalPaste(*args)

    def test_optical_drive_init(self):
        args = ["LG", 12, 24, 48, "12", "24", "48", Money("60", USD)]
        drive = OpticalDrive(*args)
        self.assertEqual(drive.model, args[0])
        self.assertEqual(drive.bluray_read_speed, args[1])
        self.assertEqual(drive.dvd_read_speed, args[2])
        self.assertEqual(drive.cd_read_speed, args[3])
        self.assertEqual(drive.bluray_write_speed, args[4])
        self.assertEqual(drive.dvd_write_speed, args[5])
        self.assertEqual(drive.cd_write_speed, args[6])
        self.assertEqual(drive.price, args[7])

    def test_opticaldrive_bad_init(self):
        args = ["LG", 12, 24, 48, 12, "24", "48", Money("60", USD)]
        with self.assertRaises(ValueError):
            _ = OpticalDrive(*args)

    def test_soundcard_init(self):
        args = ["SoundBlaster", "ATX", 5.1, 2048, 231, 96000.0, Money("60")]
        soundcard = SoundCard(*args)
        self.assertEqual(soundcard.model, args[0])
        self.assertEqual(soundcard.chipset, args[1])
        self.assertEqual(soundcard.channels, args[2])
        self.assertEqual(soundcard.bitrate, args[3])
        self.assertEqual(soundcard.snr, args[4])
        self.assertEqual(soundcard.sample_rate, args[5])
        self.assertEqual(soundcard.price, args[6])

    def test_soundcard_bad_init(self):
        args = ["SoundBlaster", "ATX", 5.1, 2048, 231, "96000", Money("60")]
        with self.assertRaises(ValueError):
            _ = SoundCard(*args)

    def test_ethernet_card_init(self):
        args = ["LG", "PCI-e x8", NetworkSpeed.from_gbits(1000), 2, Money("60", USD)]
        ethernet_card = EthernetCard(*args)
        self.assertEqual(ethernet_card.model, args[0])
        self.assertEqual(ethernet_card.interface, args[1])
        self.assertEqual(ethernet_card.port_speed, args[2])
        self.assertEqual(ethernet_card.port_number, args[3])
        self.assertEqual(ethernet_card.price, args[4])

    def test_ethernet_card_bad_init(self):
        args = ["LG", "PCI-e x8", NetworkSpeed.from_gbits(1000), "2", Money("60", USD)]
        with self.assertRaises(ValueError):
            _ = EthernetCard(*args)

    def test_wireless_card_init(self):
        args = ["Realtek", "PCI-e x8", "b/g/n/ac", Money("60", USD)]
        wireless_card = WirelessCard(*args)
        self.assertEqual(wireless_card.model, args[0])
        self.assertEqual(wireless_card.interface, args[1])
        self.assertEqual(wireless_card.supported_protocols, args[2])
        self.assertEqual(wireless_card.price, args[3])

    def test_wireless_card_bad_init(self):
        args = ["Realtek", "PCI-e x8", 802.11, Money("60", USD)]
        with self.assertRaises(ValueError):
            _ = WirelessCard(*args)

    def test_monitor_init(self):
        args = ["MSI Optix", Resolution(1920, 1080), 27, 4, "IPS", Money("300", USD)]
        monitor = Monitor(*args)
        self.assertEqual(monitor.model, args[0])
        self.assertEqual(monitor.resolution, args[1])
        self.assertEqual(monitor.size, args[2])
        self.assertEqual(monitor.response_time, args[3])
        self.assertEqual(monitor.panel_type, args[4])
        self.assertEqual(monitor.price, args[5])

    def test_monitor_bad_init(self):
        args = ["MSI Optix", Resolution(1920, 1080), 27, 4, 1, Money("300", USD)]
        with self.assertRaises(ValueError):
            _ = Monitor(*args)

    def test_externalhdd_init(self):
        args = ["Seagate", "Barracuda", "2000", Bytes.from_tb(3), Money("0.09", USD), Money("80", USD)]
        hdd = ExternalHDD(*args)
        self.assertEqual(hdd.model, args[0])
        self.assertEqual(hdd.model_line, args[1])
        self.assertEqual(hdd.type, args[2])
        self.assertEqual(hdd.capacity, args[3])
        self.assertEqual(hdd.price_per_gb, args[4])
        self.assertEqual(hdd.price, args[5])

    def test_externalhdd_bad_init(self):
        args = ["Seagate", "Barracuda", 2000, Bytes.from_tb(3), Money("0.09", USD), Money("80", USD)]
        with self.assertRaises(ValueError):
            _ = ExternalHDD(*args)

    def test_headphones_init(self):
        args = ["Audio-Technica", "Overear", False, False, FrequencyResponse(48, 128000, 24000),
                Money("150.00", USD)]
        headphones = Headphones(*args)
        self.assertEqual(headphones.model, args[0])
        self.assertEqual(headphones.type, args[1])
        self.assertEqual(headphones.has_microphone, args[2])
        self.assertEqual(headphones.is_wireless, args[3])
        self.assertEqual(headphones.frequency_response, args[4])
        self.assertEqual(headphones.price, args[5])

    def test_headphones_bad_init(self):
        args = ["Audio-Technica", "Overear", False, 1, FrequencyResponse(48, 128000, 24000),
                Money("150.00", USD)]
        with self.assertRaises(ValueError):
            _ = Headphones(*args)

    def test_keyboard_init(self):
        args = ["Cooler Master MX-50", "Mechanical", "Red", "Cherry MX", "RGB", Money("100", USD)]
        keyboard = Keyboard(*args)
        self.assertEqual(keyboard.model, args[0])
        self.assertEqual(keyboard.style, args[1])
        self.assertEqual(keyboard.color, args[2])
        self.assertEqual(keyboard.switch_type, args[3])
        self.assertEqual(keyboard.backlight_type, args[4])
        self.assertEqual(keyboard.price, args[5])

    def test_keyboard_bad_init(self):
        args = ["Cooler Master MX-50", "Mechanical", "Red", "Cherry MX", 100, Money("100", USD)]
        with self.assertRaises(ValueError):
            _ = Keyboard(*args)

    def test_mouse_init(self):
        args = ["Logitech G903", "optical", "wireless", "black", Money("113.00", USD)]
        mouse = Mouse(*args)
        self.assertEqual(mouse.model, args[0])
        self.assertEqual(mouse.type, args[1])
        self.assertEqual(mouse.connection, args[2])
        self.assertEqual(mouse.color, args[3])
        self.assertEqual(mouse.price, args[4])

    def test_mouse_bad_init(self):
        args = ["Logitech G903", 100, "wireless", "black", Money("113.00", USD)]
        with self.assertRaises(ValueError):
            _ = Mouse(*args)

    def test_speakers_init(self):
        args = ["Logitech", 5.1, 89.0, FrequencyResponse(96, 48000, 21000), Money("80", USD)]
        speakers = Speakers(*args)
        self.assertEqual(speakers.model, args[0])
        self.assertEqual(speakers.channel_configuration, args[1])
        self.assertEqual(speakers.wattage, args[2])
        self.assertEqual(speakers.frequency_response, args[3])
        self.assertEqual(speakers.price, args[4])

    def test_speakers_bad_init(self):
        args = ["Logitech", 5.1, "89", FrequencyResponse(96, 48000, 21000), Money("80", USD)]
        with self.assertRaises(ValueError):
            _ = Speakers(*args)

    def test_ups_init(self):
        args = ["PowerMaster", 1200, 24, Money("200", USD)]
        ups = UPS(*args)
        self.assertEqual(ups.model, args[0])
        self.assertEqual(ups.watt_capacity, args[1])
        self.assertEqual(ups.va_capacity, args[2])
        self.assertEqual(ups.price, args[3])

    def test_ups_bad_init(self):
        args = ["PowerMaster", 1200, "24", Money("200", USD)]
        with self.assertRaises(ValueError):
            _ = UPS(*args)
