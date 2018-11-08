from dataclasses import dataclass
from decimal import Decimal

"""
    Author: Jonathan Vusich

    These classes are general purpose dataclasses designed to hold
    and represent data collected from https://pcpartpicker.com. 
"""


@dataclass
class CPU:
    """CPU dataclass."""
    _name: str
    """str: The make and model of this CPU."""
    _cores: int
    """int: The number of cores that this CPU has (excludes hyperthreading + SMT)."""
    _tdp: int
    """int: The TDP of this CPU."""
    _clock_speed: str
    """str: The clock speed of this CPU."""
    _price: Decimal
    """Decimal: The price of this CPU."""

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
    def clock_speed(self):
        return self._clock_speed

    @property
    def price(self):
        return self._price


@dataclass
class CPUCooler:
    """CPU Cooler dataclass."""
    _name: str
    """str: The make and model of this CPU cooler."""
    _fan_rpm: str
    """str: The RPM of the fans found on this CPU cooler."""
    _decibels: str
    """str: The number of decibels produced by this CPU cooler."""
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
    """Motherboard dataclass."""
    _name: str
    """str: The make and model of this motherboard"""
    _socket: str
    """str: The CPU socket type on this motherboard"""
    _form_factor: str
    """str: The form factor of this motherboard"""
    _ram_slots: int
    """int: The number of RAM slots on this motherboard"""
    _max_ram: str
    """str: The maximum amount of RAM that this motherboard supports (given in GB)"""
    _price: Decimal
    """Decimal: The price of this motherboard."""

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
    def ram_slots(self):
        return self._ram_slots

    @property
    def max_ram(self):
        return self._max_ram

    @property
    def price(self):
        return self._price


@dataclass
class Memory:
    """Memory dataclass."""
    _name: str
    """str: The make and model of this memory module"""
    _type: str
    """str: The type and frequency of this memory module"""
    _module_type: str
    """str: The module type of this memory module"""
    _cas_timing: int
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
    def cas_timing(self):
        return self._cas_timing

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
    """HDD dataclass."""
    _name: str
    """str: The make and model of this HDD"""
    _model_line: str
    """str: The model line of this HDD"""
    _form_factor: str
    """str: The form factor of this HDD"""
    _platter_rpm: int
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
    def model_line(self):
        return self._model_line

    @property
    def form_factor(self):
        return self._form_factor

    @property
    def platter_rpm(self):
        return self._platter_rpm

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
    """SSD dataclass."""
    _name: str
    """str: The make and model of this SSD"""
    _model_line: str
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
    def model_line(self):
        return self._model_line

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


class GPU:
    """GPU dataclass."""
    _name: str
    """str: The make and model of this GPU."""
    _model_line: str
    """str: The model line of this GPU."""
    _chipset: str
    """str: The chipset of this GPU."""
    _memory_amount: str
    """str: The amount of video memory in this GPU."""
    _core_clock: str
    """str: The clock speed of this GPU """
    _price: Decimal
    """Decimal: The price of this GPU."""

    @property
    def name(self):
        return self._name

    @property
    def model_line(self):
        return self.model_line

    @property
    def chipset(self):
        return self._chipset

    @property
    def memory_amount(self):
        return self._memory_amount

    @property
    def core_clock(self):
        return self._core_clock

    @property
    def price(self):
        return self._price


@dataclass
class PSU:
    """PSU dataclass."""
    _name: str
    """str: The name of this PSU."""
    _model_line: str
    """str: The model line of this PSU."""
    _form_factor: str
    """str: The form factor of this PSU."""
    _efficiency_rating: str
    """str: The efficiency rating of this PSU."""
    _watt_rating: int
    """str: The watt rating of this PSU."""
    _modular: str
    """str: The modular properties of this PSU."""
    _price: Decimal
    """Decimal: The price of this PSU."""

    @property
    def name(self):
        return self._name

    @property
    def model_line(self):
        return self._model_line

    @property
    def form_factor(self):
        return self._form_factor

    @property
    def efficiency_rating(self):
        return self._efficiency_rating

    @property
    def watt_rating(self):
        return self._watt_rating

    @property
    def modular(self):
        return self._modular

    @property
    def price(self):
        return self._price


@dataclass
class Case:
    """PC case dataclass."""
    _name: str
    """str: The make and model of this case."""
    _form_factor: str
    """str: The form factor of this case."""
    _external_bays: int
    """int: The number of external 5.25" bays in this case."""
    _internal_bays: int
    """int: The number of internal 3.5" bays in this case."""
    _price: Decimal
    """Decimal: The price of this case."""
    _psu_wattage: int
    """int: The wattage amount of the internal PSU of this case.
            If no PSU is present, this value will be set to None."""

    @property
    def name(self):
        return self._name

    @property
    def form_factor(self):
        return self._form_factor

    @property
    def external_bays(self):
        return self._external_bays

    @property
    def internal_bays(self):
        return self._internal_bays

    @property
    def price(self):
        return self._price

    @property
    def psu_wattage(self):
        return self._psu_wattage


@dataclass
class Fan:
    """CPU and case fan dataclass."""
    _name: str
    """str: The make and model of this fan."""
    _color: str
    """str: The color of this fan."""
    _size: int
    """int: The size of this fan in millimeters."""
    _rpm: str
    """str: The RPM or RPM range of this fan."""
    _airflow: str
    """str: The amount of airflow that this fan can produce."""
    _decibels: str
    """str: The decibel amount or range produced by this fan."""
    _price: Decimal
    """Decimal: The price of this fan."""

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def size(self):
        return self._size

    @property
    def rpm(self):
        return self._rpm

    @property
    def airflow(self):
        return self._airflow

    @property
    def decibels(self):
        return self._decibels

    @property
    def price(self):
        return self._price


@dataclass
class FanController:
    """Fan controller dataclass."""
    _name: str
    """str: The make and model of this fan controller."""
    _form_factor: str
    """str: The form factor of this fan controller."""
    _channels: str
    """str: The number of fans that this fan controller can control."""
    _channel_wattage: str
    """str: The number of watts that this fan can provide to each channel."""
    _price: Decimal
    """Decimal: The price of this fan controller."""

    @property
    def name(self):
        return self._name

    @property
    def form_factor(self):
        return self._form_factor

    @property
    def channels(self):
        return self._channels

    @property
    def channel_wattage(self):
        return self._channel_wattage

    @property
    def price(self):
        return self._price


@dataclass
class ThermalPaste:
    """Thermal paste dataclass."""
    _name: str
    """str: The make and model of this thermal paste."""
    _amount: Decimal
    """Decimal: The amount of thermal paste provided in this product (in grams)."""
    _price: Decimal
    """Decimal: The price of this thermal paste."""

    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount

    @property
    def price(self):
        return self._price


@dataclass
class OpticalDrive:
    """Optical drive dataclass."""
    _name: str
    """str: The make and model of this optical drive."""
    _bluray_read_speed: int
    """int: The BluRay read speed of this optical drive."""
    _dvd_read_speed: int
    """int: The DVD read speed of this optical drive."""
    _cd_read_speed: int
    """int: The CD read speed of this optical drive."""
    _bluray_write_speed: str
    """str: The BluRay write speeds of this optical drive."""
    _dvd_write_speed: str
    """str: The DVD write speeds of this optical drive."""
    _cd_write_speed: str
    """str: The CD write speeds of this optical drive."""
    _price: Decimal
    """Decimal: The price of this optical drive."""

    @property
    def name(self):
        return self._name

    @property
    def bluray_read_speed(self):
        return self._bluray_read_speed

    @property
    def dvd_read_speed(self):
        return self._dvd_read_speed

    @property
    def cd_read_speed(self):
        return self._cd_read_speed

    @property
    def bluray_write_speed(self):
        return self._bluray_write_speed

    @property
    def dvd_write_speed(self):
        return self._dvd_write_speed

    @property
    def cd_write_speed(self):
        return self._cd_write_speed

    @property
    def price(self):
        return self._price


@dataclass
class SoundCard:
    """Sound card dataclass."""
    _name: str
    """str: The make and model of this sound card."""
    _chipset: str
    """str: The chipset of this sound card."""
    _channels: Decimal
    """Decimal: The channels provided by this sound card."""
    _bitrate: int
    """int: The bitrate of this sound card."""
    _snr: int
    """int: The signal to noise ratio of this sound card."""
    _sample_rate: int
    """int: The sample rate of this sound card."""
    _price: Decimal
    """Decimal: The price of this sound card."""

    @property
    def name(self):
        return self._name

    @property
    def chipset(self):
        return self._chipset

    @property
    def channels(self):
        return self._channels

    @property
    def bitrate(self):
        return self._bitrate

    @property
    def snr(self):
        return self._snr

    @property
    def sample_rate(self):
        return self._sample_rate

    def price(self):
        return self._price


# TODO: Finish writing the rest of these dataclasses!