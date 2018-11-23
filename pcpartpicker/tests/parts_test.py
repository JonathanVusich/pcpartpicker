import pytest
from pcpartpicker.parts import *
from moneyed import Money, USD


def test_check_typing():
    check_typing(12, int)
    with pytest.raises(ValueError):
        check_typing(12.3, int)
    check_typing(None, int)


def test_bytes_init():
    size = Bytes(50)
    assert size.total == 50
    assert size.KB == 0.05
    assert size.MB == 0.00005
    assert size.GB == 0.00000005
    assert size.TB == 0.00000000005
    assert size.PB == 0.00000000000005


def test_bytes_bad_init():
    with pytest.raises(ValueError):
        _ = Bytes("50")


def test_bytes_from_kb():
    size = Bytes.from_KB(50)
    assert size.total == 50000
    assert size.KB == 50
    assert size.MB == 0.05
    assert size.GB == 0.00005
    assert size.TB == 0.00000005
    assert size.PB == 0.00000000005


def test_bytes_from_mb():
    size = Bytes.from_MB(50)
    assert size.total == 50000000
    assert size.KB == 50000
    assert size.MB == 50
    assert size.GB == 0.05
    assert size.TB == 0.00005
    assert size.PB == 0.00000005


def test_bytes_from_gb():
    size = Bytes.from_GB(50)
    assert size.total == 50000000000
    assert size.KB == 50000000
    assert size.MB == 50000
    assert size.GB == 50
    assert size.TB == 0.05
    assert size.PB == 0.00005


def test_bytes_from_tb():
    size = Bytes.from_TB(50)
    assert size.total == 50000000000000
    assert size.KB == 50000000000
    assert size.MB == 50000000
    assert size.GB == 50000
    assert size.TB == 50
    assert size.PB == 0.05


def test_bytes_from_pb():
    size = Bytes.from_PB(50)
    assert size.total == 50000000000000000
    assert size.KB == 50000000000000
    assert size.MB == 50000000000
    assert size.GB == 50000000
    assert size.TB == 50000
    assert size.PB == 50


def test_resolution_init():
    resolution = Resolution(1920, 1080)
    assert resolution.width == 1920
    assert resolution.height == 1080


def test_resolution_bad_init():
    with pytest.raises(ValueError):
        _ = Resolution("1920", "1080")


def test_clock_speed_init():
    clock_speed = ClockSpeed(3450000000)
    assert clock_speed.MHz == 3450
    assert clock_speed.GHz == 3.45


def test_clock_speed_bad_init():
    with pytest.raises(ValueError):
        _ = ClockSpeed("This is a test")


def test_clock_speed_from_GHz_float():
    clock_speed = ClockSpeed.from_GHz(3.45)
    assert clock_speed.MHz == 3450
    assert clock_speed.GHz == 3.45
    assert clock_speed.cycles == 3450000000


def test_clock_speed_from_GHz_str():
    clock_speed = ClockSpeed.from_GHz("3.45")
    assert clock_speed.MHz == 3450
    assert clock_speed.GHz == 3.45
    assert clock_speed.cycles == 3450000000


def test_clock_speed_from_GHz_bad_str():
    with pytest.raises(ValueError):
        _ = ClockSpeed.from_GHz("This is a test")

def test_clock_speed_from_MHz_float():
    clock_speed = ClockSpeed.from_MHz(3450)
    assert clock_speed.MHz == 3450
    assert clock_speed.GHz == 3.45
    assert clock_speed.cycles == 3450000000


def test_clock_speed_from_MHz_str():
    clock_speed = ClockSpeed.from_MHz("3450")
    assert clock_speed.MHz == 3450
    assert clock_speed.GHz == 3.45
    assert clock_speed.cycles == 3450000000


def test_clock_speed_from_MHz_bad_str():
    with pytest.raises(ValueError):
        _ = ClockSpeed.from_MHz("this is a test")


def test_decibel_init():
    decibels = Decibels(12.5, 34.5, 22)
    assert decibels.min == 12.5
    assert decibels.max == 34.5
    assert decibels.default == 22


def test_decibel_bad_init():
    with pytest.raises(ValueError):
        args = ["12.5", "34.5", "23.1"]
        _ = Decibels(*args)


def test_rpm_init():
    args = [12.5, 34.5, 22]
    rpm = RPM(*args)
    assert rpm.min == args[0]
    assert rpm.max == args[1]
    assert rpm.default == args[2]


def test_rpm_bad_init():
    with pytest.raises(ValueError):
        args = ["12.5", "34.5", "23.1"]
        _ = RPM(*args)


def test_cfm_init():
    args = [12.5, 34.5, 22]
    cfm = CFM(*args)
    assert cfm.min == args[0]
    assert cfm.max == args[1]
    assert cfm.default == args[2]


def test_cfm_bad_init():
    args = ["12.5", "34.5", "23.1"]
    with pytest.raises(ValueError):
        _ = CFM(*args)


def test_network_speed_init():
    network_speed = NetworkSpeed(2000)
    assert network_speed.bits_per_second == 2000


def test_network_speed_bad_init():
    with pytest.raises(ValueError):
        _ = NetworkSpeed.from_Gbits("2")


def test_network_speed_from_mbits():
    network_speed = NetworkSpeed.from_Mbits(1000)
    assert network_speed.Mbits == 1000
    assert network_speed.Gbits == 1


def test_network_speed_from_gbits():
    network_speed = NetworkSpeed.from_Gbits(2)
    assert network_speed.Mbits == 2000
    assert network_speed.Gbits == 2


def test_cpu_init():
    args = ["Intel Core i7-6700k", ClockSpeed.from_GHz(4.4), 4, 95, Money("230.00", USD)]
    cpu = CPU(*args)
    assert cpu.model == args[0]
    assert cpu.clock_speed == args[1]
    assert cpu.cores == args[2]
    assert cpu.tdp == args[3]
    assert cpu.price == args[4]


def test_cpu_bad_init():
    args = [6700, ClockSpeed.from_GHz("4.4"), 4, 95, Money("230.00", USD)]
    with pytest.raises(ValueError):
        _ = CPU(*args)


def test_cpu_cooler_init():
    args = ["Cooler Master Hyper 212 Evo", RPM(500, 2400, 1800), Decibels(12.2, 43.8, 30.2), Money("25.99", USD)]
    cpu_cooler = CPUCooler(*args)
    assert cpu_cooler.model == args[0]
    assert cpu_cooler.fan_rpm == args[1]
    assert cpu_cooler.decibels == args[2]
    assert cpu_cooler.price == args[3]


def test_cpu_cooler_bad_init():
    args = ["Cooler Master Hyper 212 Evo", 5000, Decibels(12.2, 43.8, 30.2), Money("25.99", USD)]
    with pytest.raises(ValueError):
        _ = CPUCooler(*args)


def test_motherboard_init():
    args = ["MSI Z170", "Z170", "ATX", 2, Bytes.from_GB(8), Money("89.11", USD)]
    mobo = Motherboard(*args)
    assert mobo.model == args[0]
    assert mobo.socket == args[1]
    assert mobo.form_factor == args[2]
    assert mobo.ram_slots == args[3]
    assert mobo.max_ram == args[4]
    assert mobo.price == args[5]


def test_motherboard_bad_init():
    args = ["MSI Z170", "Z170", "ATX", "2", Bytes.from_GB(8), Money("89.11", USD)]
    with pytest.raises(ValueError):
        _ = Motherboard(*args)


def test_memory_init():
    args = ["Corsair Vengeance", "DDR4", ClockSpeed.from_MHz("3000"), "288-pin DIMM", 15,
            2, Bytes.from_GB(8), Bytes.from_GB(16), Money("0.22", USD), Money("122.45", USD)]
    memory = Memory(*args)
    assert memory.model == args[0]
    assert memory.module_type == args[1]
    assert memory.speed == args[2]
    assert memory.form_factor == args[3]
    assert memory.cas_timing == args[4]
    assert memory.number_of_modules == args[5]
    assert memory.module_size == args[6]
    assert memory.total_size == args[7]
    assert memory.price_per_gb == args[8]
    assert memory.price == args[9]


def test_memory_bad_init():
    args = ["Corsair Vengeance", "DDR4", ClockSpeed.from_MHz("3000"), "288-pin DIMM", 15,
            2, Bytes.from_GB(8), Bytes.from_GB(16), 0.22, Money("122.45", USD)]
    with pytest.raises(ValueError):
        _ = Memory(*args)


def test_storage_drive_init():
    args = ["Seagate", "WD Black", "2.5 in", "HDD", None, Bytes.from_TB(4), Bytes.from_MB(256), Money("0.08", USD), Money("123.00", USD)]
    hdd = StorageDrive(*args)
    assert hdd.model == args[0]
    assert hdd.model_line == args[1]
    assert hdd.form_factor == args[2]
    assert hdd.type == args[3]
    assert hdd.platter_rpm == args[4]
    assert hdd.capacity == args[5]
    assert hdd.cache_amount == args[6]
    assert hdd.price_per_gb == args[7]
    assert hdd.price == args[8]


def test_storage_drive_bad_init():
    args = ["Seagate", "WD Black", "2.5 in", 7200, None, Bytes.from_TB(4), Bytes.from_MB(256), Money("0.08", USD),
            Money("123.00", USD)]
    with pytest.raises(ValueError):
        _ = StorageDrive(*args)


def test_gpu_init():
    args = ["EVGA", "RTX 2080", "T104", Bytes.from_GB(8), ClockSpeed.from_GHz(2), Money("300.00", USD)]
    gpu = GPU(*args)
    assert gpu.model == args[0]
    assert gpu.model_line == args[1]
    assert gpu.chipset == args[2]
    assert gpu.memory_amount == args[3]
    assert gpu.core_clock == args[4]
    assert gpu.price == args[5]


def test_gpu_bad_init():
    args = ["EVGA", "RTX 2080", 104, Bytes.from_GB(8), ClockSpeed.from_GHz(2), Money("300.00", USD)]
    with pytest.raises(ValueError):
        _ = GPU(*args)


def test_psu_init():
    args = ["EVGA", "G1", "ATX", "80+ Gold", 800, "Fully modular", Money("120", USD)]
    psu = PSU(*args)
    assert psu.model == args[0]
    assert psu.model_line == args[1]
    assert psu.form_factor == args[2]
    assert psu.efficiency_rating == args[3]
    assert psu.watt_rating == args[4]
    assert psu.modular == args[5]
    assert psu.price == args[6]


def test_psu_bad_init():
    args = ["EVGA", "G1", "ATX", 80, 800, "Fully modular", Money("120", USD)]
    with pytest.raises(ValueError):
        _ = PSU(*args)


def test_case_init():
    args = ["Lian Li", "ATX", 4, 4, None, Money("120", USD)]
    case = Case(*args)
    assert case.model == args[0]
    assert case.form_factor == args[1]
    assert case.external_bays == args[2]
    assert case.internal_bays == args[3]
    assert case.psu_wattage == args[4]


def test_case_bad_init():
    args = ["Lian Li", "ATX", 4, 4, "435", Money("120", USD)]
    with pytest.raises(ValueError):
        _ = Case(*args)


def test_fan_init():
    args = ["Cooler Master", "black", 120, RPM(800, 2500, 1800), CFM(4, 21, 16), Decibels(21, 45, 33),
            Money("23.34", USD)]
    fan = Fan(*args)
    assert fan.model == args[0]
    assert fan.color == args[1]
    assert fan.size == args[2]
    assert fan.rpm == args[3]
    assert fan.airflow == args[4]
    assert fan.decibels == args[5]
    assert fan.price == args[6]


def test_fan_bad_init():
    args = ["Cooler Master", True, 120, RPM(800, 2500, 1800), CFM(4, 21, 16), Decibels(21, 45, 33),
            Money("23.34", USD)]
    with pytest.raises(ValueError):
        _ = Fan(*args)


def test_fan_controller_init():
    args = ["Cooler Master", "5.25\'", 5, 12, Money("60.00", USD)]
    fan_controller = FanController(*args)
    assert fan_controller.model == args[0]
    assert fan_controller.form_factor == args[1]
    assert fan_controller.channels == args[2]
    assert fan_controller.channel_wattage == args[3]
    assert fan_controller.price == args[4]


def test_fan_controller_bad_init():
    args = ["Cooler Master", "5.25\'", 5, "12", Money("60.00", USD)]
    with pytest.raises(ValueError):
        _ = FanController(*args)


def test_thermalpaste_init():
    args = ["Cooler Master", 23, Money("23.45", USD)]
    thermalpaste = ThermalPaste(*args)
    assert thermalpaste.model == args[0]
    assert thermalpaste.amount == args[1]
    assert thermalpaste.price == args[2]


def test_thermalpaste_bad_init():
    args = ["Cooler Master", "23", Money("23.45", USD)]
    with pytest.raises(ValueError):
        _ = ThermalPaste(*args)


def test_opticaldrive_init():
    args = ["LG", 12, 24, 48, "12", "24", "48", Money("60", USD)]
    drive = OpticalDrive(*args)
    assert drive.model == args[0]
    assert drive.bluray_read_speed == args[1]
    assert drive.dvd_read_speed == args[2]
    assert drive.cd_read_speed == args[3]
    assert drive.bluray_write_speed == args[4]
    assert drive.dvd_write_speed == args[5]
    assert drive.cd_write_speed == args[6]
    assert drive.price == args[7]


def test_opticaldrive_bad_init():
    args = ["LG", 12, 24, 48, 12, "24", "48", Money("60", USD)]
    with pytest.raises(ValueError):
        _ = OpticalDrive(*args)


def test_soundcard_init():
    args = ["SoundBlaster", "ATX", 5.1, 2048, 231, 96000.0, Money("60")]
    soundcard = SoundCard(*args)
    assert soundcard.model == args[0]
    assert soundcard.chipset == args[1]
    assert soundcard.channels == args[2]
    assert soundcard.bitrate == args[3]
    assert soundcard.snr == args[4]
    assert soundcard.sample_rate == args[5]
    assert soundcard.price == args[6]


def test_soundcard_bad_init():
    args = ["SoundBlaster", "ATX", 5.1, 2048, 231, "96000", Money("60")]
    with pytest.raises(ValueError):
        _ = SoundCard(*args)


def test_ethernet_card_init():
    args = ["LG", "PCI-e x8", NetworkSpeed.from_Gbits(1000), 2, Money("60", USD)]
    ethernet_card = EthernetCard(*args)
    assert ethernet_card.model == args[0]
    assert ethernet_card.interface == args[1]
    assert ethernet_card.port_speed == args[2]
    assert ethernet_card.port_number == args[3]
    assert ethernet_card.price == args[4]


def test_ethernet_card_bad_init():
    args = ["LG", "PCI-e x8", NetworkSpeed.from_Gbits(1000), "2", Money("60", USD)]
    with pytest.raises(ValueError):
        _ = EthernetCard(*args)


def test_wireless_card_init():
    args = ["Realtek", "PCI-e x8", "b/g/n/ac", Money("60", USD)]
    wireless_card = WirelessCard(*args)
    assert wireless_card.model == args[0]
    assert wireless_card.interface == args[1]
    assert wireless_card.supported_protocols == args[2]
    assert wireless_card.price == args[3]


def test_wireless_card_bad_init():
    args = ["Realtek", "PCI-e x8", 802.11, Money("60", USD)]
    with pytest.raises(ValueError):
        _ = WirelessCard(*args)


def test_monitor_init():
    args = ["MSI Optix", Resolution(1920, 1080), 27, 4, True, Money("300", USD)]
    monitor = Monitor(*args)
    assert monitor.model == args[0]
    assert monitor.resolution == args[1]
    assert monitor.size == args[2]
    assert monitor.response_time == args[3]
    assert monitor.ips == args[4]
    assert monitor.price == args[5]


def test_monitor_bad_init():
    args = ["MSI Optix", Resolution(1920, 1080), 27, 4, 1, Money("300", USD)]
    with pytest.raises(ValueError):
        _ = Monitor(*args)


def test_externalhdd_init():
    args = ["Seagate", "Barracuda", "2000", Bytes.from_TB(3), Money("0.09", USD), Money("80", USD)]
    hdd = ExternalHDD(*args)
    assert hdd.model == args[0]
    assert hdd.model_line == args[1]
    assert hdd.type == args[2]
    assert hdd.capacity == args[3]
    assert hdd.price_per_gb == args[4]
    assert hdd.price == args[5]


def test_externalhdd_bad_init():
    args = ["Seagate", "Barracuda", 2000, Bytes.from_TB(3), Money("0.09", USD), Money("80", USD)]
    with pytest.raises(ValueError):
        _ = ExternalHDD(*args)


def test_headphones_init():
    args = ["Audio-Technica", "Overear", False, False, FrequencyResponse(48, 128000, 24000),
            Money("150.00", USD)]
    headphones = Headphones(*args)
    assert headphones.model == args[0]
    assert headphones.type == args[1]
    assert headphones.has_microphone == args[2]
    assert headphones.is_wireless == args[3]
    assert headphones.frequency_response == args[4]
    assert headphones.price == args[5]


def test_headphones_bad_init():
    args = ["Audio-Technica", "Overear", False, 1, FrequencyResponse(48, 128000, 24000),
            Money("150.00", USD)]
    with pytest.raises(ValueError):
        _ = Headphones(*args)


def test_keyboard_init():
    args = ["Cooler Master MX-50", "Mechanical", "Red", "Cherry MX", "RGB", Money("100", USD)]
    keyboard = Keyboard(*args)
    assert keyboard.model == args[0]
    assert keyboard.style == args[1]
    assert keyboard.color == args[2]
    assert keyboard.switch_type == args[3]
    assert keyboard.backlight_type == args[4]
    assert keyboard.price == args[5]


def test_keyboard_bad_init():
    args = ["Cooler Master MX-50", "Mechanical", "Red", "Cherry MX", 100, Money("100", USD)]
    with pytest.raises(ValueError):
        _ = Keyboard(*args)


def test_mouse_init():
    args = ["Logitech G903", "optical", "wireless", "black", Money("113.00", USD)]
    mouse = Mouse(*args)
    assert mouse.model == args[0]
    assert mouse.type == args[1]
    assert mouse.connection == args[2]
    assert mouse.color == args[3]
    assert mouse.price == args[4]


def test_mouse_bad_init():
    args = ["Logitech G903", 100, "wireless", "black", Money("113.00", USD)]
    with pytest.raises(ValueError):
        _ = Mouse(*args)


def test_speakers_init():
    args = ["Logitech", 5.1, 89.0, FrequencyResponse(96, 48000, 21000), Money("80", USD)]
    speakers = Speakers(*args)
    assert speakers.model == args[0]
    assert speakers.channel_configuration == args[1]
    assert speakers.wattage == args[2]
    assert speakers.frequency_response == args[3]
    assert speakers.price == args[4]


def test_speakers_bad_init():
    args = ["Logitech", 5.1, "89", FrequencyResponse(96, 48000, 21000), Money("80", USD)]
    with pytest.raises(ValueError):
        _ = Speakers(*args)


def test_ups_init():
    args = ["PowerMaster", 1200, 24, Money("200", USD)]
    ups = UPS(*args)
    assert ups.model == args[0]
    assert ups.watt_capacity == args[1]
    assert ups.va_capacity == args[2]
    assert ups.price == args[3]


def test_ups_bad_init():
    args = ["PowerMaster", 1200, "24", Money("200", USD)]
    with pytest.raises(ValueError):
        _ = UPS(*args)
