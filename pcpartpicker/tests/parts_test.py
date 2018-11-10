import pytest
from pcpartpicker.parts import *

# Bytes class tests
def test_bytes_init():
    bytes = Bytes(Decimal("50"))
    assert(bytes.num == Decimal("50"))
    assert(bytes.KB == Decimal("0.05"))
    assert(bytes.MB == Decimal("0.00005"))
    assert(bytes.GB == Decimal("0.00000005"))
    assert(bytes.TB == Decimal("0.00000000005"))
    assert(bytes.PB == Decimal("0.00000000000005"))

    bytes = Bytes.from_KB(Decimal("50"))
    assert(bytes.num == Decimal("50000"))
    assert(bytes.KB == Decimal("50"))
    assert(bytes.MB == Decimal("0.05"))
    assert(bytes.GB == Decimal("0.00005"))
    assert(bytes.TB == Decimal("0.00000005"))
    assert(bytes.PB == Decimal("0.00000000005"))

    bytes = Bytes.from_MB(Decimal("50"))
    assert(bytes.num == Decimal("50000000"))
    assert(bytes.KB == Decimal("50000"))
    assert(bytes.MB == Decimal("50"))
    assert(bytes.GB == Decimal("0.05"))
    assert(bytes.TB == Decimal("0.00005"))
    assert(bytes.PB == Decimal("0.00000005"))

    bytes = Bytes.from_GB(Decimal("50"))
    assert(bytes.num == Decimal("50000000000"))
    assert(bytes.KB == Decimal("50000000"))
    assert(bytes.MB == Decimal("50000"))
    assert(bytes.GB == Decimal("50"))
    assert(bytes.TB == Decimal("0.05"))
    assert(bytes.PB == Decimal("0.00005"))

    bytes = Bytes.from_TB(Decimal("50"))
    assert(bytes.num == Decimal("50000000000000"))
    assert(bytes.KB == Decimal("50000000000"))
    assert(bytes.MB == Decimal("50000000"))
    assert(bytes.GB == Decimal("50000"))
    assert(bytes.TB == Decimal("50"))
    assert(bytes.PB == Decimal("0.05"))

    bytes = Bytes.from_PB(Decimal("50"))
    assert(bytes.num == Decimal("50000000000000000"))
    assert(bytes.KB == Decimal("50000000000000"))
    assert(bytes.MB == Decimal("50000000000"))
    assert(bytes.GB == Decimal("50000000"))
    assert(bytes.TB == Decimal("50000"))
    assert(bytes.PB == Decimal("50"))


def test_bytes_repr():
    bytes = Bytes(Decimal("50"))
    assert(repr(bytes) == "Bytes(_num=Decimal(\'50\'))")


# Resolution class tests
def test_resolution_init():
    resolution = Resolution(1920, 1080)
    assert(resolution.width == 1920)
    assert(resolution.height == 1080)
    assert(resolution.pixel_count == 2073600)


# Clockspeed class tests
def test_clockspeed_init():
    clockspeed = ClockSpeed(Decimal("3450000000"))
    assert(clockspeed.MHz == Decimal("3450"))
    assert(clockspeed.GHz == Decimal("3.45"))

    clockspeed = ClockSpeed.from_GHz(Decimal("3.45"))
    assert (clockspeed.MHz == Decimal("3450"))
    assert(clockspeed.GHz == Decimal("3.45"))
    assert(clockspeed.cycles == Decimal("3450000000"))


# CPU class tests
def test_cpu_init():
    args = ["Intel i7-6700k", Decimal("230.00"), 4, 95, Decimal("4.4")]
    cpu = CPU(*args)
    assert(cpu.name == args[0])
    assert(cpu.price == args[1])
    assert(cpu.cores == args[2])
    assert(cpu.tdp == args[3])
    assert(cpu.clock_speed == args[4])