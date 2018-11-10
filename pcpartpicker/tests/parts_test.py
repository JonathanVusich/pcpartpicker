import pytest
from pcpartpicker.parts import *

# Bytes class tests
def test_bytes_init():
    bytes = Bytes(50)
    assert(bytes.num == 50)
    assert(bytes.KB == 0.05)
    assert(bytes.MB == 0.00005)
    assert(bytes.GB == 0.00000005)
    assert(bytes.TB == 0.00000000005)
    assert(bytes.PB == 0.00000000000005)


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


def test_bytes_repr():
    bytes = Bytes(50)
    assert(repr(bytes) == "Bytes(_num=50)")


# Resolution class tests
def test_resolution_init():
    resolution = Resolution(1920, 1080)
    assert(resolution.width == 1920)
    assert(resolution.height == 1080)
    assert(resolution.pixel_count == 2073600)


# Clockspeed class tests
def test_clockspeed_init():
    clockspeed = ClockSpeed(3450000000)
    assert(clockspeed.MHz == 3450)
    assert(clockspeed.GHz == 3.45)


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


def test_rpm_init():
    args = [12.5, 34.5, 22]
    rpm = RPM(*args)
    assert(rpm.min == args[0])
    assert(rpm.max == args[1])
    assert(rpm.default == args[2])


# CPU class tests
def test_cpu_init():
    args = ["Intel i7-6700k", Decimal("230.00"), 4, 95, Decimal("4.4")]
    cpu = CPU(*args)
    assert(cpu.name == args[0])
    assert(cpu.price == args[1])
    assert(cpu.cores == args[2])
    assert(cpu.tdp == args[3])
    assert(cpu.clock_speed == args[4])