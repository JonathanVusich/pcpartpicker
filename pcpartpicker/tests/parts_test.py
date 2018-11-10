import pytest
from pcpartpicker.parts import *


def test_check_typing():
    check_typing(12, int)
    with pytest.raises(ValueError):
        check_typing(12.3, int)
    check_typing(None, int)


# Bytes class tests
def test_bytes_init():
    bytes = Bytes(50)
    assert(bytes.num == 50)
    assert(bytes.KB == 0.05)
    assert(bytes.MB == 0.00005)
    assert(bytes.GB == 0.00000005)
    assert(bytes.TB == 0.00000000005)
    assert(bytes.PB == 0.00000000000005)


def test_bytes_bad_init():
    with pytest.raises(ValueError):
        bytes = Bytes("50")


def test_bytes_from_kb():
    bytes = Bytes.from_KB(50)
    assert(bytes.num == 50000)
    assert(bytes.KB == 50)
    assert(bytes.MB == 0.05)
    assert(bytes.GB == 0.00005)
    assert(bytes.TB == 0.00000005)
    assert(bytes.PB == 0.00000000005)


def test_bytes_from_mb():
    bytes = Bytes.from_MB(50)
    assert(bytes.num == 50000000)
    assert(bytes.KB == 50000)
    assert(bytes.MB == 50)
    assert(bytes.GB == 0.05)
    assert(bytes.TB == 0.00005)
    assert(bytes.PB == 0.00000005)


def test_bytes_from_gb():
    bytes = Bytes.from_GB(50)
    assert(bytes.num == 50000000000)
    assert(bytes.KB == 50000000)
    assert(bytes.MB == 50000)
    assert(bytes.GB == 50)
    assert(bytes.TB == 0.05)
    assert(bytes.PB == 0.00005)


def test_bytes_from_tb():
    bytes = Bytes.from_TB(50)
    assert(bytes.num == 50000000000000)
    assert(bytes.KB == 50000000000)
    assert(bytes.MB == 50000000)
    assert(bytes.GB == 50000)
    assert(bytes.TB == 50)
    assert(bytes.PB == 0.05)


def test_bytes_from_pb():
    bytes = Bytes.from_PB(50)
    assert(bytes.num == 50000000000000000)
    assert(bytes.KB == 50000000000000)
    assert(bytes.MB == 50000000000)
    assert(bytes.GB == 50000000)
    assert(bytes.TB == 50000)
    assert(bytes.PB == 50)


# Part class tests
def test_part_init():
    part = Part("Test", Decimal("23.12"))
    assert(part.name == "Test")
    assert(part.price == Decimal("23.12"))


def test_part_bad_init():
    with pytest.raises(ValueError):
        part = Part("Hi there", 23.12)


# Resolution class tests
def test_resolution_init():
    resolution = Resolution(1920, 1080)
    assert(resolution.width == 1920)
    assert(resolution.height == 1080)
    assert(resolution.pixel_count == 2073600)


def test_resolution_bad_init():
    with pytest.raises(ValueError):
        resolution = Resolution("1920", "1080")


# Clockspeed class tests
def test_clockspeed_init():
    clockspeed = ClockSpeed(3450000000)
    assert(clockspeed.MHz == 3450)
    assert(clockspeed.GHz == 3.45)


def test_clockspeed_bad_init():
    with pytest.raises(ValueError):
        clockspeed = ClockSpeed("3450000000")


def test_clockspeed_from_GHz():
    clockspeed = ClockSpeed.from_GHz(3.45)
    assert (clockspeed.MHz == 3450)
    assert(clockspeed.GHz == 3.45)
    assert(clockspeed.cycles == 3450000000)


def test_clockspeed_from_MHz():
    clockspeed = ClockSpeed.from_MHz(3450)
    assert(clockspeed.MHz == 3450)
    assert(clockspeed.GHz == 3.45)
    assert(clockspeed.cycles == 3450000000)


# Decibel class test
def test_decibel_init():
    args = [12.5, 34.5, 22]
    decibels = Decibels(*args)
    assert(decibels.min == args[0])
    assert(decibels.max == args[1])
    assert(decibels.default == args[2])


def test_decibel_bad_init():
    with pytest.raises(ValueError):
        args = ["12.5", "34.5", "23.1"]
        decibels = Decibels(*args)


# RPM class test
def test_rpm_init():
    args = [12.5, 34.5, 22]
    rpm = RPM(*args)
    assert(rpm.min == args[0])
    assert(rpm.max == args[1])
    assert(rpm.default == args[2])


def test_rpm_bad_init():
    with pytest.raises(ValueError):
        args = ["12.5", "34.5", "23.1"]
        rpm = RPM(*args)


# CFM class test
def test_cfm_init():
    args = [12.5, 34.5, 22]
    cfm = CFM(*args)
    assert(cfm.min == args[0])
    assert(cfm.max == args[1])
    assert(cfm.default == args[2])


def test_cfm_bad_init():
    with pytest.raises(ValueError):
        args = ["12.5", "34.5", "23.1"]
        cfm = CFM(*args)



# CPU class tests
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
        cpu = CPU(*args)


# CPU cooler tests
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
        cpu_cooler = CPUCooler(*args)


# Motherboard data class tests
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
        mobo = Motherboard(*args)


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
        memory = Memory(*args)


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
        hdd = StorageDrive(*args)


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
        hdd = HDD(*args)


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
        ssd = SSD(*args)


