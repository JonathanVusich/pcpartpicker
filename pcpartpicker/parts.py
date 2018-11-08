from dataclasses import dataclass
from decimal import Decimal

"""
    These classes are general purpose dataclasses designed to hold
    and represent data collected from https://pcpartpicker.com. 
"""


@dataclass
class CPU:
    """CPU dataclass"""
    _name: str
    """str: The make and model of this CPU"""
    _cores: int
    """int: The number of cores that this CPU has (excludes hyperthreading + SMT)"""
    _tdp: int
    """int: The TDP of this CPU"""
    _speed: Decimal
    """Decimal: The clock speed of this CPU (in GHz)"""
    _price: Decimal
    """Decimal: The price of this CPU"""

    @property
    def name(self):
        return self._name

    @property
    def cores(self):
        return self._cores

    @property
    def tdp(self):
        return self._tdp

    @property
    def speed(self):
        return self._speed

    @property
    def price(self):
        return self._price


@dataclass
class CPUCooler:
    """CPU Cooler dataclass"""
    _name: str
    """str: The make and model of this CPU cooler"""
    _fan_rpm: str
    """The RPM range of this CPU cooler"""
    _decibels: str
    """str: The decibel range produced by this CPU cooler"""
    _price: Decimal
    """Decimal: The price of this CPU cooler"""

    @property
    def name(self):
        return self._name

    @property
    def fan_rpm(self):
        return self._fan_rpm

    @property
    def decibels(self):
        return self._decibels

    @property
    def price(self):
        return self._price


@dataclass
class Motherboard:
    """Motherboard dataclass"""
    _name: str
    """str: The make and model of this motherboard"""
    _socket: str
    """str: The CPU socket type on this motherboard"""
    _form_factor: str
    """str: The form factor of this motherboard"""
    _RAM_slots: int
    """int: The number of RAM slots on this motherboard"""
    _max_RAM: int
    """int: The maximum amount of RAM that this motherboard supports (given in GB)"""

    @property
    def name(self):
        return self._name

    @property
    def socket(self):
        return self._socket

    @property
    def form_factor(self):
        return self._form_factor

    @property
    def RAM_slots(self):
        return self._RAM_slots

    @property
    def max_RAM(self):
        return self._max_RAM

    @property
    def price(self):
        return self._price


@dataclass
class Memory:
    """Memory dataclass (RAM)"""
    _name: str
    """str: The make and model of this memory module"""
    _type: str
    """str: The type and frequency of this memory module"""
    _module_type: str
    """str: The module type of this memory module"""
    _CAS_timing: int
    """int: The CAS timing of this memory module"""
    _number_of_modules: int
    """int: The number of modules that come with this memory configuration"""
    _module_size: str
    """str: The size of the modules that come with this memory configuration"""
    _price_per_gb: Decimal
    """Decimal: The price per GB for this memory configuration"""
    _price: Decimal
    """Decimal: The price for this memory configuration"""

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def module_type(self):
        return self._module_type

    @property
    def CAS_timing(self):
        return self._CAS_timing

    @property
    def number_of_modules(self):
        return self._number_of_modules

    @property
    def module_size(self):
        return self._module_size

    @property
    def price_per_gb(self):
        return self._price_per_gb

    @property
    def price(self):
        return self._price


@dataclass
class HDD:
    """HDD dataclass (mechanical only)"""
    _name: str
    """str: The make and model of this HDD"""
    _series: str
    """str: The model line of this HDD"""
    _form_factor: str
    """str: The form factor of this HDD"""
    _speed: int
    """int: The platter RPM of this HDD"""
    _capacity: str
    """str: The capacity of this HDD"""
    _cache_amount: str
    """str: The cache amount found in this HDD"""
    _price: Decimal
    """Decimal: The price for this HDD"""

    @property
    def name(self):
        return self._name

    @property
    def series(self):
        return self._series

    @property
    def form_factor(self):
        return self._form_factor

    @property
    def speed(self):
        return self._speed

    @property
    def capacity(self):
        return self._capacity

    @property
    def cache_amount(self):
        return self._cache_amount

    @property
    def price(self):
        return self._price


@dataclass
class SSD:
    """SSD dataclass"""
    _name: str
    """str: The make and model of this SSD"""
    _series: str
    """str: The model line of this SSD"""
    _form_factor: str
    """str: The form factor of this SSD"""
    _capacity: str
    """str: The capacity of this SSD"""
    _cache_amount: str
    """str: The cache amount found in this SSD"""
    _price: Decimal
    """Decimal: The price of this SSD"""

    @property
    def name(self):
        return self._name

    @property
    def series(self):
        return self._series

    @property
    def form_factor(self):
        return self._form_factor

    @property
    def capacity(self):
        return self._capacity

    @property
    def cache_amount(self):
        return self._cache_amount

    @property
    def price(self):
        return self._price


# TODO: Finish writing the rest of these dataclasses!