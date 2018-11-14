import pytest
from pcpartpicker.parts import *


def test_check_typing():
    check_typing(12, int)
    with pytest.raises(ValueError):
        check_typing(12.3, int)
    check_typing(None, int)


def test_bytes_init():
    size = Bytes(50)
    assert(size.num == 50)
    assert(size.KB == 0.05)
    assert(size.MB == 0.00005)
    assert(size.GB == 0.00000005)
    assert(size.TB == 0.00000000005)
    assert(size.PB == 0.00000000000005)


def test_bytes_bad_init():
    with pytest.raises(ValueError):
        _ = Bytes("50")


def test_bytes_from_kb():
    size = Bytes.from_KB(50)
    assert(size.num == 50000)
    assert(size.KB == 50)
    assert(size.MB == 0.05)
    assert(size.GB == 0.00005)
    assert(size.TB == 0.00000005)
    assert(size.PB == 0.00000000005)


def test_bytes_from_mb():
    size = Bytes.from_MB(50)
    assert(size.num == 50000000)
    assert(size.KB == 50000)
    assert(size.MB == 50)
    assert(size.GB == 0.05)
    assert(size.TB == 0.00005)
    assert(size.PB == 0.00000005)


def test_bytes_from_gb():
    size = Bytes.from_GB(50)
    assert(size.num == 50000000000)
    assert(size.KB == 50000000)
    assert(size.MB == 50000)
    assert(size.GB == 50)
    assert(size.TB == 0.05)
    assert(size.PB == 0.00005)


def test_bytes_from_tb():
    size = Bytes.from_TB(50)
    assert(size.num == 50000000000000)
    assert(size.KB == 50000000000)
    assert(size.MB == 50000000)
    assert(size.GB == 50000)
    assert(size.TB == 50)
    assert(size.PB == 0.05)


def test_bytes_from_pb():
    size = Bytes.from_PB(50)
    assert(size.num == 50000000000000000)
    assert(size.KB == 50000000000000)
    assert(size.MB == 50000000000)
    assert(size.GB == 50000000)
    assert(size.TB == 50000)
    assert(size.PB == 50)


def test_part_init():
    part = Part("Test", Decimal("23.12"))
    assert(part.name == "Test")
    assert(part.price == Decimal("23.12"))


def test_part_bad_init():
    with pytest.raises(ValueError):
        _ = Part("Hi there", 23.12)


def test_resolution_init():
    resolution = Resolution(1920, 1080)
    assert(resolution.width == 1920)
    assert(resolution.height == 1080)
    assert(resolution.pixel_count == 2073600)


def test_resolution_bad_init():
    with pytest.raises(ValueError):
        _ = Resolution("1920", "1080")


def test_clock_speed_init():
    clock_speed = ClockSpeed(3450000000)
    assert(clock_speed.MHz == 3450)
    assert(clock_speed.GHz == 3.45)


def test_clock_speed_bad_init():
    with pytest.raises(ValueError):
        _ = ClockSpeed("3450000000")


def test_clock_speed_from_GHz():
    clock_speed = ClockSpeed.from_GHz(3.45)
    assert (clock_speed.MHz == 3450)
    assert(clock_speed.GHz == 3.45)
    assert(clock_speed.cycles == 3450000000)


def test_clock_speed_from_MHz():
    clock_speed = ClockSpeed.from_MHz(3450)
    assert(clock_speed.MHz == 3450)
    assert(clock_speed.GHz == 3.45)
    assert(clock_speed.cycles == 3450000000)


def test_decibel_init():
    decibels = Decibels(12.5, 34.5, 22)
    assert(decibels.min == 12.5)
    assert(decibels.max == 34.5)
    assert(decibels.default == 22)


def test_decibel_bad_init():
    with pytest.raises(ValueError):
        args = ["12.5", "34.5", "23.1"]
        _ = Decibels(*args)


def test_rpm_init():
    args = [12.5, 34.5, 22]
    rpm = RPM(*args)
    assert(rpm.min == args[0])
    assert(rpm.max == args[1])
    assert(rpm.default == args[2])


def test_rpm_bad_init():
    with pytest.raises(ValueError):
        args = ["12.5", "34.5", "23.1"]
        _ = RPM(*args)


def test_cfm_init():
    args = [12.5, 34.5, 22]
    cfm = CFM(*args)
    assert(cfm.min == args[0])
    assert(cfm.max == args[1])
    assert(cfm.default == args[2])


def test_cfm_bad_init():
    args = ["12.5", "34.5", "23.1"]
    with pytest.raises(ValueError):
        _ = CFM(*args)


def test_cpu_init():
    args = ["Intel Core i7-6700k", Decimal("230.00"), 4, 95, ClockSpeed.from_GHz(4.4)]
    cpu = CPU(*args)
    assert(cpu.name == args[0])
    assert(cpu.price == args[1])
    assert(cpu.cores == args[2])
    assert(cpu.tdp == args[3])
    assert(cpu.clock_speed == args[4])


def test_cpu_bad_init():
    args = [6700, Decimal("230.00"), 4, 95, ClockSpeed.from_GHz(4.4)]
    with pytest.raises(ValueError):
        _ = CPU(*args)


def test_cpu_cooler_init():
    args = ["Cooler Master Hyper 212 Evo", Decimal("25.99"), RPM(500, 2400, 1800), Decibels(12.2, 43.8, 30.2)]
    cpu_cooler = CPUCooler(*args)
    assert(cpu_cooler.name == args[0])
    assert(cpu_cooler.price == args[1])
    assert(cpu_cooler.fan_rpm == args[2])
    assert(cpu_cooler.decibels == args[3])


def test_cpu_cooler_bad_init():
    args = ["Cooler Master Hyper 212 Evo", Decimal("25.99"), 5000, Decibels(12.2, 43.8, 30.2)]
    with pytest.raises(ValueError):
        _ = CPUCooler(*args)


def test_motherboard_init():
    args = ["MSI Z170", Decimal("89.11"), "Z170", "ATX", 2, Bytes.from_GB(8)]
    mobo = Motherboard(*args)
    assert(mobo.name == args[0])
    assert(mobo.price == args[1])
    assert(mobo.socket == args[2])
    assert(mobo.form_factor == args[3])
    assert(mobo.ram_slots == args[4])
    assert(mobo.max_ram == args[5])


def test_motherboard_bad_init():
    args = ["MSI Z170", Decimal("89.11"), "Z170", "ATX", "2", Bytes.from_GB(8)]
    with pytest.raises(ValueError):
        _ = Motherboard(*args)


def test_memory_init():
    args = ["Corsair Vengeance", Decimal("122.45"), "288-pin DIMM", ClockSpeed.from_GHz(3), "DDR4", 15, 2, Bytes.from_GB(4), Bytes.from_GB(8), 0.08]
    memory = Memory(*args)
    assert(memory.name == args[0])
    assert(memory.price == args[1])
    assert(memory.type == args[2])
    assert(memory.speed == args[3])
    assert(memory.module_type == args[4])
    assert(memory.cas_timing == args[5])
    assert(memory.number_of_modules == args[6])
    assert(memory.module_size == args[7])
    assert(memory.total_size == args[8])
    assert(memory.price_per_gb == args[9])


def test_memory_bad_init():
    args = ["Corsair Vengeance", Decimal("122.45"), "288-pin DIMM", ClockSpeed.from_GHz(3), "DDR4", 15, 2,
            Bytes.from_GB(4), Bytes.from_GB(8), Decimal("0.08")]
    with pytest.raises(ValueError):
        _ = Memory(*args)


def test_storage_drive_init():
    args = ["Seagate", Decimal("80.00"), "WD Black", "2.5 in", Bytes.from_TB(4), Bytes.from_MB(256)]
    hdd = StorageDrive(*args)
    assert(hdd.name == args[0])
    assert(hdd.price == args[1])
    assert(hdd.model_line == args[2])
    assert(hdd.form_factor == args[3])
    assert(hdd.capacity == args[4])
    assert(hdd.cache_amount == args[5])


def test_storage_drive_bad_init():
    args = [123, Decimal("80.00"), "WD Black", "2.5 in", Bytes.from_TB(4), Bytes.from_MB(256)]
    with pytest.raises(ValueError):
        _ = StorageDrive(*args)


def test_hdd_init():
    args = ["Seagate", Decimal("80.00"), "WD Black", "2.5 in", Bytes.from_TB(4), Bytes.from_MB(256), 7200]
    hdd = HDD(*args)
    assert(hdd.name == args[0])
    assert(hdd.price == args[1])
    assert(hdd.model_line == args[2])
    assert(hdd.form_factor == args[3])
    assert(hdd.capacity == args[4])
    assert(hdd.cache_amount == args[5])
    assert(hdd.platter_rpm == args[6])


def test_hdd_bad_init():
    args = ["Seagate", Decimal("80.00"), "WD Black", "2.5 in", Bytes.from_TB(4), Bytes.from_MB(256), "7200"]
    with pytest.raises(ValueError):
        _ = HDD(*args)


def test_ssd_init():
    args = ["Seagate", Decimal("80.00"), "WD Black", "2.5 in", Bytes.from_TB(4), Bytes.from_MB(256)]
    ssd = SSD(*args)
    assert(ssd.name == args[0])
    assert(ssd.price == args[1])
    assert(ssd.model_line == args[2])
    assert(ssd.form_factor == args[3])
    assert(ssd.capacity == args[4])
    assert(ssd.cache_amount == args[5])


def test_ssd_bad_init():
    args = [1234, Decimal("80.00"), "WD Black", "2.5 in", Bytes.from_TB(4), Bytes.from_MB(256)]
    with pytest.raises(ValueError):
        _ = SSD(*args)


def test_hybriddrive_init():
    args = ["Seagate", Decimal("80.00"), "WD Black", "2.5 in", Bytes.from_TB(4), Bytes.from_MB(256)]
    hybrid_drive = HybridDrive(*args)
    assert (hybrid_drive.name == args[0])
    assert (hybrid_drive.price == args[1])
    assert (hybrid_drive.model_line == args[2])
    assert (hybrid_drive.form_factor == args[3])
    assert (hybrid_drive.capacity == args[4])
    assert (hybrid_drive.cache_amount == args[5])


def test_hybriddrive_bad_init():
    args = ["Seagate", Decimal("80.00"), "WD Black", "2.5 in", Bytes.from_TB(4), 256]
    with pytest.raises(ValueError):
        _ = HybridDrive(*args)


def test_gpu_init():
    args = ["EVGA", Decimal("500"), "RTX 2080", "T104", Bytes.from_GB(8), ClockSpeed.from_GHz(2)]
    gpu = GPU(*args)
    assert(gpu.name == args[0])
    assert(gpu.price == args[1])
    assert(gpu.model_line == args[2])
    assert(gpu.chipset == args[3])
    assert(gpu.memory_amount == args[4])
    assert(gpu.core_clock == args[5])


def test_gpu_bad_init():
    args = ["EVGA", 500, "RTX 2080", "T104", Bytes.from_GB(8), ClockSpeed.from_GHz(2)]
    with pytest.raises(ValueError):
        _ = GPU(*args)


def test_psu_init():
    args = ["EVGA", Decimal("120"), "G1", "ATX", "80+ Gold", 800, "Fully modular"]
    psu = PSU(*args)
    assert(psu.name == args[0])
    assert(psu.price == args[1])
    assert(psu.model_line == args[2])
    assert(psu.form_factor == args[3])
    assert(psu.efficiency_rating == args[4])
    assert(psu.watt_rating == args[5])
    assert(psu.modular == args[6])


def test_psu_bad_init():
    args = ["EVGA", Decimal("120"), "G1", "ATX", "80+ Gold", "800", "Fully modular"]
    with pytest.raises(ValueError):
        _ = PSU(*args)

def test_case_init():
    args = ["Lian Li", Decimal("120"), "ATX", 4, 4, None]
    case = Case(*args)
    assert(case.name == args[0])
    assert(case.price == args[1])
    assert(case.form_factor == args[2])
    assert(case.external_bays == args[3])
    assert(case.internal_bays == args[4])
    assert(case.psu_wattage == args[5])


def test_case_bad_init():
    args = ["Lian Li", 120, "ATX", 4, 4, None]
    with pytest.raises(ValueError):
        _ = Case(*args)


def test_fan_init():
    args = ["Cooler Master", Decimal("23.34"), "black", 120, RPM(800, 2500, 1800), CFM(4, 21, 16), Decibels(21, 45, 33)]
    fan = Fan(*args)
    assert(fan.name == args[0])
    assert(fan.price == args[1])
    assert(fan.color == args[2])
    assert(fan.size == args[3])
    assert(fan.rpm == args[4])
    assert(fan.airflow == args[5])
    assert(fan.decibels == args[6])


def test_fan_bad_init():
    args = ["Cooler Master", Decimal("23.34"), "black", "120", RPM(800, 2500, 1800), CFM(4, 21, 16), Decibels(21, 45, 33)]
    with pytest.raises(ValueError):
        _ = Fan(*args)


def test_fan_controller_init():
    args = ["Cooler Master", Decimal("60"), "5.25\'", 5, 12]
    fan_controller = FanController(*args)
    assert(fan_controller.name == args[0])
    assert(fan_controller.price == args[1])
    assert(fan_controller.form_factor == args[2])
    assert(fan_controller.channels == args[3])
    assert(fan_controller.channel_wattage == args[4])


def test_fan_controller_bad_init():
    args = ["Cooler Master", 60, "5.25\'", 5, 12]
    with pytest.raises(ValueError):
        _ = FanController(*args)


def test_thermalpaste_init():
    args = ["Cooler Master", Decimal("23.45"), 23]
    thermalpaste = ThermalPaste(*args)
    assert(thermalpaste.name == args[0])
    assert(thermalpaste.price == args[1])
    assert(thermalpaste.amount == args[2])


def test_thermalpaste_bad_init():
    args = ["Cooler Master", Decimal("23.45"), "23"]
    with pytest.raises(ValueError):
        _ = ThermalPaste(*args)


def test_opticaldrive_init():
    args = ["LG", Decimal("60"), 12, 24, 48, "12", "24", "48"]
    drive = OpticalDrive(*args)
    assert(drive.name == args[0])
    assert(drive.price == args[1])
    assert(drive.bluray_read_speed == args[2])
    assert(drive.dvd_read_speed == args[3])
    assert(drive.cd_read_speed == args[4])
    assert(drive.bluray_write_speed == args[5])
    assert(drive.dvd_write_speed == args[6])
    assert(drive.cd_write_speed == args[7])


def test_opticaldrive_bad_init():
    args = ["LG", Decimal("60"), 12, 24, 48, 12, "24", "48"]
    with pytest.raises(ValueError):
        _ = OpticalDrive(*args)


def test_soundcard_init():
    args = ["SoundBlaster", Decimal("60"), "ATX", 5.1, 2048, 231, 96000]
    soundcard = SoundCard(*args)
    assert(soundcard.name == args[0])
    assert(soundcard.price == args[1])
    assert(soundcard.chipset == args[2])
    assert(soundcard.channels == args[3])
    assert(soundcard.bitrate == args[4])
    assert(soundcard.snr == args[5])
    assert(soundcard.sample_rate == args[6])


def test_soundcard_bad_init():
    args = ["SoundBlaster", Decimal("60"), 1234, 5.1, 2048, 231, 96000]
    with pytest.raises(ValueError):
        _ = SoundCard(*args)


def test_ethernet_card_init():
    args = ["LG", Decimal("60"), "PCI-e x8", "1000 Gbit/s", 2]
    ethernet_card = EthernetCard(*args)
    assert(ethernet_card.name == args[0])
    assert(ethernet_card.price == args[1])
    assert(ethernet_card.interface == args[2])
    assert(ethernet_card.port_speed == args[3])
    assert(ethernet_card.port_number == args[4])


def test_ethernet_card_bad_init():
    args = ["LG", 60, "PCI-e x8", "1000 Mbit/s", 2]
    with pytest.raises(ValueError):
        _ = EthernetCard(*args)


def test_wireless_card_init():
    args = ["Realtek", Decimal("60"), "PCI-e x8", "b/g/n/ac"]
    wireless_card = WirelessCard(*args)
    assert(wireless_card.name == args[0])
    assert(wireless_card.price == args[1])
    assert(wireless_card.interface == args[2])
    assert(wireless_card.supported_protocols == args[3])


def test_wireless_card_bad_init():
    args = ["Realtek", 60, "PCI-e x8", "b/g/n/ac"]
    with pytest.raises(ValueError):
        _ = WirelessCard(*args)


def test_monitor_init():
    args = ["MSI Optix", Decimal("300"), Resolution(1920, 1080), 27, 4, True]
    monitor = Monitor(*args)
    assert(monitor.name == args[0])
    assert(monitor.price == args[1])
    assert(monitor.resolution == args[2])
    assert(monitor.size == args[3])
    assert(monitor.response_time == args[4])
    assert(monitor.ips == args[5])


def test_monitor_bad_init():
    args = ["MSI Optix", 300, Resolution(1920, 1080), 27, 4, True]
    with pytest.raises(ValueError):
        _ = Monitor(*args)



def test_externalhdd_init():
    args = ["Seagate", Decimal("80"), "Barracuda", "2000", Bytes.from_TB(3), .09]
    hdd = ExternalHDD(*args)
    assert(hdd.name == args[0])
    assert(hdd.price == args[1])
    assert(hdd.model == args[2])
    assert(hdd.type == args[3])
    assert(hdd.capacity == args[4])
    assert(hdd.price_per_gb == args[5])


def test_externalhdd_bad_init():
    args = ["Seagate", Decimal("80"), "Barracuda", 2000, Bytes.from_TB(3), .09]
    with pytest.raises(ValueError):
        _ = ExternalHDD(*args)


def test_headphones_init():
    args = ["Audio-Technica", Decimal("150"), "Overear", False, False, FrequencyResponse(48, 128000, 24000)]
    headphones = Headphones(*args)
    assert(headphones.name == args[0])
    assert(headphones.price == args[1])
    assert(headphones.type == args[2])
    assert(headphones.has_microphone == args[3])
    assert(headphones.is_wireless == args[4])
    assert(headphones.frequency_response == args[5])


def test_headphones_bad_init():
    args = ["Audio-Technica", Decimal("150"), "Overear", "No", False, FrequencyResponse(48, 128000, 24000)]
    with pytest.raises(ValueError):
        _ = Headphones(*args)


def test_keyboard_init():
    args = ["Cooler Master MX-50", Decimal("100"), "Mechanical", "Red", "Cherry MX", "RGB"]
    keyboard = Keyboard(*args)
    assert(keyboard.name == args[0])
    assert(keyboard.price == args[1])
    assert(keyboard.style == args[2])
    assert(keyboard.color == args[3])
    assert(keyboard.switch_type == args[4])
    assert(keyboard.backlight_type == args[5])


def test_keyboard_bad_init():
    args = ["Cooler Master MX-50", 100, "Mechanical", "Red", "Cherry MX", "RGB"]
    with pytest.raises(ValueError):
        _ = Keyboard(*args)


def test_mouse_init():
    args = ["Logitech G903", Decimal("150"), "optical", "wireless", "black"]
    mouse = Mouse(*args)
    assert(mouse.name == args[0])
    assert(mouse.price == args[1])
    assert(mouse.type == args[2])
    assert(mouse.connection == args[3])
    assert(mouse.color == args[4])


def test_mouse_bad_init():
    args = ["Logitech G903", 150, "optical", "wireless", "black"]
    with pytest.raises(ValueError):
        _ = Mouse(*args)


def test_speakers_init():
    args = ["Logitech", Decimal("60"), 5.1, 89, FrequencyResponse(96, 48000, 21000)]
    speakers = Speakers(*args)
    assert(speakers.name == args[0])
    assert(speakers.price == args[1])
    assert(speakers.channel_configuration == args[2])
    assert(speakers.wattage == args[3])
    assert(speakers.frequency_response == args[4])


def test_speakers_bad_init():
    args = ["Logitech", 60, 5.1, 89, FrequencyResponse(96, 48000, 21000)]
    with pytest.raises(ValueError):
        _ = Speakers(*args)


def test_ups_init():
    args = ["PowerMaster", Decimal("200"), 1200, 24]
    ups = UPS(*args)
    assert(ups.name == args[0])
    assert(ups.price == args[1])
    assert(ups.watt_capacity == args[2])
    assert(ups.va_capacity == args[3])


def test_ups_bad_init():
    args = ["PowerMaster", Decimal("200"), 1200, "24"]
    with pytest.raises(ValueError):
        _ = UPS(*args)
