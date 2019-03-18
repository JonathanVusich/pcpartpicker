from dataclasses import dataclass
from typing import Union

from moneyed import Money

from .utils import num

"""
    Author: Jonathan Vusich

    These classes are general purpose dataclasses designed to hold
    and represent specification data for computer hardware. 
"""


def check_typing(attribute, class_type):
    """"""
    if attribute:
        if not isinstance(attribute, class_type):
            raise ValueError(f"'{attribute}' must be of type '{class_type}'!")


@dataclass(frozen=True)
class Range:
    """Base dataclass for different types of data ranges."""
    min: Union[float, int]
    """float: The minimum value for this range."""
    max: Union[float, int]
    """float: The maximum value for this range."""
    default: Union[float, int]
    """float: The default value for this range."""

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class Resolution:
    """Dataclass that stores resolution data for monitors."""
    width: int
    """int: The number of horizontal pixels."""
    height: int
    """int: The number of vertical pixels."""

    def __post_init__(self):
        check_typing(self.width, int)
        check_typing(self.height, int)


@dataclass(frozen=True)
class Bytes:
    """Dataclass that stores byte numbers for easier user manipulation."""
    total: int
    """int: The number of bytes that this object represents."""

    def __post_init__(self):
        check_typing(self.total, int)

    @property
    def kb(self):
        return self.total / 1000

    @property
    def mb(self):
        return self.total / 1000000

    @property
    def gb(self):
        return self.total / 1000000000

    @property
    def tb(self):
        return self.total / 1000000000000

    @property
    def pb(self):
        return self.total / 1000000000000000

    @classmethod
    def from_kb(cls, number):
        if isinstance(number, str):
            number = num(number)
        else:
            check_typing(number, (float, int))
        num_bytes = int(number * 1000)
        return cls(num_bytes)

    @classmethod
    def from_mb(cls, number):
        if isinstance(number, str):
            number = num(number)
        else:
            check_typing(number, (float, int))
        num_bytes = int(number * 1000000)
        return cls(num_bytes)

    @classmethod
    def from_gb(cls, number):
        if isinstance(number, str):
            number = num(number)
        else:
            check_typing(number, (float, int))
        num_bytes = int(number * 1000000000)
        return cls(num_bytes)

    @classmethod
    def from_tb(cls, number):
        if isinstance(number, str):
            number = num(number)
        else:
            check_typing(number, (float, int))
        num_bytes = int(number * 1000000000000)
        return cls(num_bytes)

    @classmethod
    def from_pb(cls, number):
        if isinstance(number, str):
            number = num(number)
        else:
            check_typing(number, (float, int))
        num_bytes = int(number * 1000000000000000)
        return cls(num_bytes)


@dataclass(frozen=True)
class RPM(Range):
    """Dataclass that stores RPM data for computer parts."""
    min: Union[float, int, None]
    """float: The minimum value for this range."""
    max: Union[float, int, None]
    """float: The maximum value for this range."""
    default: Union[float, int, None]
    """float: The default value for this range."""

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class Decibels(Range):
    """Dataclass that stores RPM data for computer parts."""
    min: Union[float, int, None]
    """float: The minimum value for this range."""
    max: Union[float, int, None]
    """float: The maximum value for this range."""
    default: Union[float, int, None]
    """float: The default value for this range."""

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class CFM(Range):
    """Dataclass that stores RPM data for computer parts."""
    min: Union[float, int, None]
    """float: The minimum value for this range."""
    max: Union[float, int, None]
    """float: The maximum value for this range."""
    default: Union[float, int, None]
    """float: The default value for this range."""

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class FrequencyResponse(Range):
    """Dataclass that stores RPM data for computer parts."""
    min: Union[float, int, None]
    """float: The minimum value for this range."""
    max: Union[float, int, None]
    """float: The maximum value for this range."""
    default: Union[float, int, None]
    """float: The default value for this range."""

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class ClockSpeed:
    """Dataclass that stores clock speed data for various parts."""
    cycles: int
    """int: The total number of clock cycles per second."""

    def __post_init__(self):
        check_typing(self.cycles, int)

    @property
    def mhz(self):
        return self.cycles / 1000000.0

    @property
    def ghz(self):
        return self.cycles / 1000000000.0

    @classmethod
    def from_ghz(cls, number):
        if isinstance(number, str):
            number = num(number)
        else:
            check_typing(number, (float, int))
        return cls(int(number * 1000000000))

    @classmethod
    def from_mhz(cls, number):
        if isinstance(number, str):
            number = num(number)
        else:
            check_typing(number, (float, int))
        return cls(int(number * 1000000))


@dataclass(frozen=True)
class NetworkSpeed:
    """Dataclass that stores network speed data."""

    bits_per_second: int
    """int: The total number of bits per second."""

    def __post_init__(self):
        check_typing(self.bits_per_second, int)

    @property
    def mbits(self):
        return self.bits_per_second / 1000000.0

    @property
    def gbits(self):
        return self.bits_per_second / 1000000000.0

    @classmethod
    def from_gbits(cls, number: float):
        check_typing(number, (float, int))
        return cls(int(number * 1000000000))

    @classmethod
    def from_mbits(cls, number: float):
        check_typing(number, (float, int))
        return cls(int(number * 1000000))


@dataclass(frozen=True)
class CPU:
    """CPU dataclass."""

    brand: str
    """str: The brand of this CPU."""
    model: str
    """str: The model of this CPU."""
    clock_speed: ClockSpeed
    """Clockspeed: The clock speed of this CPU (in GHz)."""
    cores: int
    """int: The number of cores that this CPU has (excludes hyperthreading + SMT)."""
    tdp: int
    """int: The TDP of this CPU."""
    price: Money
    """Money: The price of the CPU."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.clock_speed, ClockSpeed)
        check_typing(self.cores, int)
        check_typing(self.tdp, int)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class CPUCooler:
    """CPU Cooler dataclass."""

    brand: str
    """str: The brand of this CPU cooler."""
    model: str
    """str: The model of this CPU cooler."""
    fan_rpm: RPM
    """RPM: The RPM information of this CPU cooler."""
    decibels: Decibels
    """Decibels: The decibel information of this CPU cooler."""
    price: Money
    """Money: The price of the CPU cooler."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.fan_rpm, RPM)
        check_typing(self.decibels, Decibels)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Motherboard:
    """Motherboard dataclass."""

    brand: str
    """str: The brand of this motherboard."""
    model: str
    """str: The model of this motherboard."""
    socket: str
    """str: The CPU socket type on this motherboard"""
    form_factor: str
    """str: The form factor of this motherboard"""
    ram_slots: int
    """int: The number of RAM slots on this motherboard"""
    max_ram: Bytes
    """Bytes: The maximum amount of RAM that this motherboard supports (given in GB)"""
    price: Money
    """Money: The price of this motherboard."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.socket, str)
        check_typing(self.form_factor, str)
        check_typing(self.ram_slots, int)
        check_typing(self.max_ram, Bytes)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Memory:
    """Memory dataclass."""

    brand: str
    """str: The brand of this memory module."""
    model: str
    """str: The model of this memory module."""
    module_type: str
    """str: The module type of this memory module"""
    speed: ClockSpeed
    """ClockSpeed: The operating frequency of this memory module."""
    form_factor: str
    """str: The form factor of this memory module."""
    cas_timing: int
    """int: The CAS timing of this memory module"""
    number_of_modules: int
    """int: The number of modules in this memory configuration."""
    module_size: Bytes
    """Bytes: The size of the modules that come with this memory configuration"""
    total_size: Bytes
    """Bytes: The total size of the modules combined."""
    price_per_gb: Money
    """float: The price per GB for this memory configuration"""
    price: Money
    """Money: The price of this memory module."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.module_type, str)
        check_typing(self.speed, ClockSpeed)
        check_typing(self.form_factor, str)
        check_typing(self.cas_timing, int)
        check_typing(self.number_of_modules, int)
        check_typing(self.module_size, Bytes)
        check_typing(self.total_size, Bytes)
        check_typing(self.price_per_gb, Money)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class StorageDrive:
    """Dataclass for storage devices."""

    brand: str
    """str: The brand of this storage device."""
    model: str
    """str: The model of this storage device."""
    model_line: str
    """str: The model line of this storage device."""
    form_factor: str
    """str: The form factor of this storage device."""
    type: str
    """str: The type of this storage device."""
    platter_rpm: int
    """int: The platter RPM of this storage device (if present)."""
    capacity: Bytes
    """Bytes: The capacity of this storage device."""
    cache_amount: Bytes
    """Bytes: The cache amount found in this storage device."""
    price_per_gb: Money
    price: Money
    """Money: The price of this storage device."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.model_line, str)
        check_typing(self.form_factor, str)
        check_typing(self.type, str)
        check_typing(self.platter_rpm, int)
        check_typing(self.capacity, Bytes)
        check_typing(self.cache_amount, Bytes)
        check_typing(self.price_per_gb, Money)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class GPU:
    """GPU dataclass."""

    brand: str
    """str: The brand of this GPU."""
    model: str
    """str: The model of this GPU."""
    model_line: str
    """str: The model line of this GPU."""
    chipset: str
    """str: The chipset of this GPU."""
    memory_amount: Bytes
    """Bytes: The amount of video memory in this GPU."""
    core_clock: ClockSpeed
    """ClockSpeed: The clock speed of this GPU """
    price: Money
    """Money: The price of this GPU."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.model_line, str)
        check_typing(self.chipset, str)
        check_typing(self.memory_amount, Bytes)
        check_typing(self.core_clock, ClockSpeed)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class PSU:
    """PSU dataclass."""

    brand: str
    """str: The brand of this PSU."""
    model: str
    """str: The model of this PSU."""
    model_line: str
    """str: The model line of this PSU."""
    form_factor: str
    """str: The form factor of this PSU."""
    efficiency_rating: str
    """str: The efficiency rating of this PSU."""
    watt_rating: int
    """int: The watt rating of this PSU."""
    modular: str
    """str: The modular properties of this PSU."""
    price: Money
    """Money: The price of this PSU."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.model_line, str)
        check_typing(self.form_factor, str)
        check_typing(self.efficiency_rating, str)
        check_typing(self.watt_rating, int)
        check_typing(self.modular, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Case:
    """PC case dataclass."""

    brand: str
    """str: The brand of this case."""
    model: str
    """str: The model of this case."""
    form_factor: str
    """str: The form factor of this case."""
    external_bays: int
    """int: The number of external 5.25" bays in this case."""
    internal_bays: int
    """int: The number of internal 3.5" bays in this case."""
    psu_wattage: int
    """int: The wattage amount of the internal PSU of this case.
            If no PSU is present, this value will be set to None."""
    price: Money
    """Money: The price of this GPU."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.form_factor, str)
        check_typing(self.external_bays, int)
        check_typing(self.internal_bays, int)
        check_typing(self.psu_wattage, int)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Fan:
    """CPU and case fan dataclass."""

    brand: str
    """str: The brand of this fan."""
    model: str
    """str: The model of this fan."""
    color: str
    """str: The color of this fan."""
    size: int
    """int: The size of this fan in millimeters."""
    rpm: RPM
    """RPM: The RPM or RPM range of this fan."""
    airflow: CFM
    """CFM: The amount of airflow that this fan can produce."""
    decibels: Decibels
    """Decibels: The decibel amount or range produced by this fan."""
    price: Money
    """Money: The price of this fan."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.color, str)
        check_typing(self.size, int)
        check_typing(self.rpm, RPM)
        check_typing(self.airflow, CFM)
        check_typing(self.decibels, Decibels)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class FanController:
    """Fan controller dataclass."""

    brand: str
    """str: The brand of this fan controller."""
    model: str
    """str: The model of this fan controller."""
    form_factor: str
    """str: The form factor of this fan controller."""
    channels: int
    """int: The number of fans that this fan controller can control."""
    channel_wattage: int
    """int: The number of watts that this fan can provide to each channel."""
    price: Money
    """Money: The price of this fan controller."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.form_factor, str)
        check_typing(self.channels, int)
        check_typing(self.channel_wattage, int)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class ThermalPaste:
    """Thermal paste dataclass."""

    brand: str
    """str: The brand of this thermal paste."""
    model: str
    """str: The model of this thermal paste."""
    amount: float
    """float: The amount of thermal paste provided in this product (in grams)."""
    price: Money
    """Money: The price of this thermal paste."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.amount, (float, int))
        check_typing(self.price, Money)


@dataclass(frozen=True)
class OpticalDrive:
    """Optical drive dataclass."""

    brand: str
    """str: The brand of this optical drive."""
    model: str
    """str: The model of this optical drive."""
    bluray_read_speed: int
    """int: The BluRay read speed of this optical drive."""
    dvd_read_speed: int
    """int: The DVD read speed of this optical drive."""
    cd_read_speed: int
    """int: The CD read speed of this optical drive."""
    bluray_write_speed: str
    """str: The BluRay write speeds of this optical drive."""
    dvd_write_speed: str
    """str: The DVD write speeds of this optical drive."""
    cd_write_speed: str
    """str: The CD write speeds of this optical drive."""
    price: Money
    """Money: The price of this optical drive."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.bluray_read_speed, int)
        check_typing(self.dvd_read_speed, int)
        check_typing(self.cd_read_speed, int)
        check_typing(self.bluray_write_speed, str)
        check_typing(self.dvd_write_speed, str)
        check_typing(self.cd_write_speed, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class SoundCard:
    """Sound card dataclass."""

    brand: str
    """str: The brand of this sound card."""
    model: str
    """str: The model of this sound card."""
    chipset: str
    """str: The chipset of this sound card."""
    channels: float
    """float: The channels provided by this sound card."""
    bitrate: int
    """int: The bitrate of this sound card."""
    snr: int
    """int: The signal to noise ratio of this sound card in dB."""
    sample_rate: float
    """int: The sample rate of this sound card in kHz."""
    price: Money
    """Money: The price of this sound card."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.chipset, str)
        check_typing(self.channels, (float, int))
        check_typing(self.bitrate, int)
        check_typing(self.snr, int)
        check_typing(self.sample_rate, float)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class EthernetCard:
    """Ethernet card dataclass."""

    brand: str
    """str: The brand of this Ethernet card."""
    model: str
    """str: The model of this Ethernet card."""
    interface: str
    """str: The motherboard interface of this Ethernet card."""
    port_speed: NetworkSpeed
    """NetworkSpeed: The maximum speed that this Ethernet card supports."""
    port_number: int
    """int: The number of Ethernet ports on this card."""
    price: Money
    """Money: The price of this Ethernet card."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.interface, str)
        check_typing(self.port_speed, NetworkSpeed)
        check_typing(self.port_number, int)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class WirelessCard:
    """Wireless card dataclass."""

    brand: str
    """str: The brand of this wireless card."""
    model: str
    """str: The model of this wireless card."""
    interface: str
    """str: The motherboard interface of this wireless card."""
    supported_protocols: str
    """str: The supported wireless protocols of this card."""
    price: Money
    """Money: The price of this wireless card."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.interface, str)
        check_typing(self.supported_protocols, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Monitor:
    """Monitor dataclass."""

    brand: str
    """str: The brand of this monitor."""
    model: str
    """str: The model of this monitor."""
    resolution: Resolution
    """Resolution: The pixel dimensions of this monitor."""
    size: float
    """float: The diagonal display size of this monitor in inches."""
    response_time: int
    """int: The response time of this display (in milliseconds)."""
    panel_type: str
    """bool: Returns True if the panel is an IPS display."""
    price: Money
    """Money: The price of this monitor."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.resolution, Resolution)
        check_typing(self.size, (float, int))
        check_typing(self.response_time, int)
        check_typing(self.panel_type, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class ExternalHDD:
    """External HDD dataclass."""

    brand: str
    """str: The brand of this external HDD."""
    model: str
    """str: The model of this external HDD."""
    type: str
    """str: The type of this external HDD."""
    capacity: Bytes
    """Bytes: The capacity of this external HDD."""
    price_per_gb: Money
    """float: The price per GB of storage of this external HDD."""
    price: Money
    """Money: The price of this external HDD."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.type, str)
        check_typing(self.capacity, Bytes)
        check_typing(self.price_per_gb, Money)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Headphones:
    """Headphones dataclass."""

    brand: str
    """str: The brand of this set of headphones."""
    model: str
    """str: The model of this set of headphones."""
    type: str
    """str: The type of this set of headphones."""
    has_microphone: bool
    """bool: Returns True if this set of headphones has a microphone."""
    is_wireless: bool
    """bool: Returns True if this set of headphones is wireless."""
    frequency_response: FrequencyResponse
    """str: The frequency response of this set of headphones."""
    price: Money
    """Money: The price of these headphones."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.type, str)
        check_typing(self.has_microphone, bool)
        check_typing(self.is_wireless, bool)
        check_typing(self.frequency_response, FrequencyResponse)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Keyboard:
    """Keyboard dataclass."""

    brand: str
    """str: The brand of this keyboard."""
    model: str
    """str: The model of this keyboard."""
    style: str
    """str: Describes the style of this keyboard."""
    color: str
    """str: Describes the color of this keyboard."""
    switch_type: str
    """str: Describes the type of switches that this keyboard uses."""
    backlight_type: str
    """str: Describes the available backlight on this device."""
    price: Money
    """Money: The price of this keyboard."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.style, str)
        check_typing(self.color, str)
        check_typing(self.switch_type, str)
        check_typing(self.backlight_type, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Mouse:
    """Computer mouse dataclass."""

    brand: str
    """str: The brand of this mouse."""
    model: str
    """str: The model of this mouse."""
    type: str
    """str: Describes the type of this mouse."""
    connection: str
    """str: Describes the type of connection that this mouse uses."""
    color: str
    """str: Describes the color of this mouse."""
    price: Money
    """Money: The price of this mouse."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.type, str)
        check_typing(self.connection, str)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Speakers:
    """Computer speakers dataclass."""

    brand: str
    """str: The brand of this set of computer speakers."""
    model: str
    """str: The model of this set of computer speakers."""
    channel_configuration: float
    """float: The channel configuration of this set of computer speakers."""
    wattage: (float, int)
    """int: The peak wattage of these speakers."""
    frequency_response: FrequencyResponse
    """FrequencyResponse: The frequency response of these speakers."""
    price: Money
    """Money: The price of these speakers."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.channel_configuration, (float, int))
        check_typing(self.wattage, (float, int))
        check_typing(self.frequency_response, FrequencyResponse)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class UPS:
    """UPS dataclass."""

    brand: str
    """str: The brand of this UPS."""
    model: str
    """str: The model of this UPS."""
    watt_capacity: int
    """int: The number of watts that this UPS can store."""
    va_capacity: int
    """int: The number of volt-amperes that this UPS can store."""
    price: Money
    """Money: The price of this UPS."""

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.watt_capacity, int)
        check_typing(self.va_capacity, (float, int))
        check_typing(self.price, Money)
