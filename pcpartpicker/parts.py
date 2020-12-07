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
    max: Union[float, int]
    default: Union[float, int]

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class Resolution:
    """Dataclass that stores resolution data for monitors."""
    width: int
    height: int

    def __post_init__(self):
        check_typing(self.width, int)
        check_typing(self.height, int)


@dataclass(frozen=True, order=True)
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
    max: Union[float, int, None]
    default: Union[float, int, None]

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class Decibels(Range):
    """Dataclass that stores RPM data for computer parts."""
    min: Union[float, int, None]
    max: Union[float, int, None]
    default: Union[float, int, None]

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class CFM(Range):
    """Dataclass that stores RPM data for computer parts."""
    min: Union[float, int, None]
    max: Union[float, int, None]
    default: Union[float, int, None]

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True)
class FrequencyResponse(Range):
    """Dataclass that stores RPM data for computer parts."""
    min: Union[float, int, None]
    max: Union[float, int, None]
    default: Union[float, int, None]

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))


@dataclass(frozen=True, order=True)
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


@dataclass(frozen=True, order=True)
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
    model: str
    cores: int
    base_clock: ClockSpeed
    boost_clock: ClockSpeed
    tdp: int
    integrated_graphics: str
    multithreading: bool
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.cores, int)
        check_typing(self.base_clock, ClockSpeed)
        check_typing(self.boost_clock, ClockSpeed)
        check_typing(self.tdp, int)
        check_typing(self.integrated_graphics, str)
        check_typing(self.multithreading, bool)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class CPUCooler:
    """CPU Cooler dataclass."""

    brand: str
    model: str
    fan_rpm: RPM
    decibels: Decibels
    color: str
    radiator_size: int
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.fan_rpm, RPM)
        check_typing(self.decibels, Decibels)
        check_typing(self.color, str)
        check_typing(self.radiator_size, int)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Motherboard:
    """Motherboard dataclass."""

    brand: str
    model: str
    socket: str
    form_factor: str
    ram_slots: int
    max_ram: Bytes
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.socket, str)
        check_typing(self.form_factor, str)
        check_typing(self.ram_slots, int)
        check_typing(self.max_ram, Bytes)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Memory:
    """Memory dataclass."""

    brand: str
    model: str
    module_type: str
    speed: ClockSpeed
    number_of_modules: int
    module_size: Bytes
    price_per_gb: Money
    color: str
    first_word_latency: float
    cas_timing: int
    error_correction: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.module_type, str)
        check_typing(self.speed, ClockSpeed)
        check_typing(self.number_of_modules, int)
        check_typing(self.module_size, Bytes)
        check_typing(self.price_per_gb, Money)
        check_typing(self.color, str)
        check_typing(self.first_word_latency, float)
        check_typing(self.cas_timing, int)
        check_typing(self.price, Money)
        check_typing(self.error_correction, str)

    @property
    def total_size(self):
        return Bytes(self.number_of_modules * self.module_size.total)


@dataclass(frozen=True)
class StorageDrive:
    """Dataclass for storage devices."""

    brand: str
    model: str
    capacity: Bytes
    price_per_gb: Money
    storage_type: str
    platter_rpm: int
    cache_amount: Bytes
    form_factor: str
    interface: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.capacity, Bytes)
        check_typing(self.price_per_gb, Money)
        check_typing(self.storage_type, str)
        check_typing(self.platter_rpm, int)
        check_typing(self.cache_amount, Bytes)
        check_typing(self.form_factor, str)
        check_typing(self.interface, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class GPU:
    """GPU dataclass."""

    brand: str
    model: str
    chipset: str
    vram: Bytes
    core_clock: ClockSpeed
    boost_clock: ClockSpeed
    color: str
    length: float
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.chipset, str)
        check_typing(self.vram, Bytes)
        check_typing(self.core_clock, ClockSpeed)
        check_typing(self.boost_clock, ClockSpeed)
        check_typing(self.color, str)
        check_typing(self.length, float)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class PSU:
    """PSU dataclass."""

    brand: str
    model: str
    form_factor: str
    efficiency_rating: str
    wattage: int
    modular: str
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.form_factor, str)
        check_typing(self.efficiency_rating, str)
        check_typing(self.wattage, int)
        check_typing(self.modular, str)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Case:
    """PC case dataclass."""

    brand: str
    model: str
    form_factor: str
    color: str
    psu_wattage: int
    side_panel: bool
    external_bays: int
    internal_bays: int
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.form_factor, str)
        check_typing(self.color, str)
        check_typing(self.side_panel, bool)
        check_typing(self.psu_wattage, int)
        check_typing(self.external_bays, int)
        check_typing(self.internal_bays, int)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Fan:
    """CPU and case fan dataclass."""

    brand: str
    model: str
    size: int
    color: str
    rpm: RPM
    airflow: CFM
    decibels: Decibels
    pwm: bool
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.size, int)
        check_typing(self.color, str)
        check_typing(self.rpm, RPM)
        check_typing(self.airflow, CFM)
        check_typing(self.decibels, Decibels)
        check_typing(self.pwm, bool)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class FanController:
    """Fan controller dataclass."""

    brand: str
    model: str
    channels: int
    channel_wattage: int
    pwm: bool
    form_factor: str
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.channels, int)
        check_typing(self.channel_wattage, int)
        check_typing(self.pwm, bool)
        check_typing(self.form_factor, str)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class ThermalPaste:
    """Thermal paste dataclass."""

    brand: str
    model: str
    amount: float
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.amount, (float, int))
        check_typing(self.price, Money)


@dataclass(frozen=True)
class OpticalDrive:
    """Optical drive dataclass."""

    brand: str
    model: str
    bluray_read_speed: int
    dvd_read_speed: int
    cd_read_speed: int
    bluray_write_speed: str
    dvd_write_speed: str
    cd_write_speed: str
    price: Money

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
    model: str
    channels: float
    bitrate: int
    snr: int
    sample_rate: float
    chipset: str
    interface: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.channels, (float, int))
        check_typing(self.bitrate, int)
        check_typing(self.snr, int)
        check_typing(self.sample_rate, float)
        check_typing(self.chipset, str)
        check_typing(self.interface, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class EthernetCard:
    """Ethernet card dataclass."""

    brand: str
    model: str
    interface: str
    port_speed: NetworkSpeed
    port_number: int
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.interface, str)
        check_typing(self.port_speed, NetworkSpeed)
        check_typing(self.port_number, int)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class WirelessCard:
    """Wireless card dataclass."""

    brand: str
    model: str
    supported_protocols: str
    interface: str
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.supported_protocols, str)
        check_typing(self.interface, str)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Monitor:
    """Monitor dataclass."""

    brand: str
    model: str
    size: float
    resolution: Resolution
    refresh_rate: int
    response_time: float
    panel_type: str
    aspect_ratio: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.size, (float, int))
        check_typing(self.resolution, Resolution)
        check_typing(self.refresh_rate, int)
        check_typing(self.response_time, float)
        check_typing(self.panel_type, str)
        check_typing(self.aspect_ratio, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class ExternalHDD:
    """External HDD dataclass."""

    brand: str
    model: str
    type: str
    interface: str
    capacity: Bytes
    price_per_gb: Money
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.type, str)
        check_typing(self.interface, str)
        check_typing(self.capacity, Bytes)
        check_typing(self.price_per_gb, Money)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Headphones:
    """Headphones dataclass."""

    brand: str
    model: str
    form_factor: str
    frequency_response: FrequencyResponse
    has_microphone: bool
    is_wireless: bool
    type: str
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.form_factor, str)
        check_typing(self.frequency_response, FrequencyResponse)
        check_typing(self.has_microphone, bool)
        check_typing(self.is_wireless, bool)
        check_typing(self.type, str)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Keyboard:
    """Keyboard dataclass."""

    brand: str
    model: str
    style: str
    switches: str
    backlight: str
    tenkeyless: bool
    connection: str
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.style, str)
        check_typing(self.switches, str)
        check_typing(self.backlight, str)
        check_typing(self.tenkeyless, bool)
        check_typing(self.connection, str)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Mouse:
    """Computer mouse dataclass."""

    brand: str
    model: str
    tracking: str
    connection: str
    max_dpi: int
    hand_orientation: str
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.tracking, str)
        check_typing(self.connection, str)
        check_typing(self.max_dpi, int)
        check_typing(self.hand_orientation, str)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class Speakers:
    """Computer speakers dataclass."""

    brand: str
    model: str
    channel_configuration: float
    wattage: (float, int)
    frequency_response: FrequencyResponse
    color: str
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.channel_configuration, (float, int))
        check_typing(self.wattage, (float, int))
        check_typing(self.frequency_response, FrequencyResponse)
        check_typing(self.color, str)
        check_typing(self.price, Money)


@dataclass(frozen=True)
class UPS:
    """UPS dataclass."""

    brand: str
    model: str
    watt_capacity: int
    va_capacity: int
    price: Money

    def __post_init__(self):
        check_typing(self.brand, str)
        check_typing(self.model, str)
        check_typing(self.watt_capacity, int)
        check_typing(self.va_capacity, (float, int))
        check_typing(self.price, Money)
