from dataclasses import dataclass, field
from decimal import Decimal

"""
    Author: Jonathan Vusich

    These classes are general purpose dataclasses designed to hold
    and represent specification data for computer hardware. 
"""


def check_typing(attribute, type):
    if attribute:
        if not isinstance(attribute, type):
            raise ValueError("\'{}\' must be of type \'{}\'!".format(attribute, type))


def _determine_type(type: str):
    if [x for x in type if x.isnumeric()]:
        return "HDD"
    return type



@dataclass
class Part:
    """The base dataclass for all the different types of parts."""
    _name: str
    """str: The part descriptor. Typically includes the brand, make and model."""

    def __post_init__(self):
        check_typing(self.name, str)

    @property
    def name(self):
        return self._name


@dataclass
class Range:
    """Base dataclass for different types of data ranges."""
    _min: float
    """float: The minimum value for this range."""
    _max: float
    """float: The maximum value for this range."""
    _default: float
    """float: The default value for this range."""

    def __post_init__(self):
        check_typing(self.min, (float, int))
        check_typing(self.max, (float, int))
        check_typing(self.default, (float, int))

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def default(self):
        return self._default


@dataclass
class Resolution:
    """Dataclass that stores resolution data for monitors."""
    _width: int
    """int: The number of horizontal pixels."""
    _height: int
    """int: The number of vertical pixels."""
    _pixel_count: int = field(init=False)
    """int: The total number of pixels."""

    def __post_init__(self):
        check_typing(self.width, int)
        check_typing(self.height, int)
        self._pixel_count = self.width * self.height

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def pixel_count(self):
        return self._pixel_count


@dataclass
class Bytes:
    """Dataclass that stores byte numbers for easier user manipulation."""
    _num: int
    """int: The number of bytes that this object represents."""

    def __post_init__(self):
        check_typing(self.num, int)

    @property
    def num(self):
        return self._num

    @property
    def KB(self):
        return self._num / 1000

    @property
    def MB(self):
        return self._num / 1000000

    @property
    def GB(self):
        return self._num / 1000000000

    @property
    def TB(self):
        return self._num / 1000000000000

    @property
    def PB(self):
        return self._num / 1000000000000000

    @classmethod
    def from_KB(cls, num: float):
        check_typing(num, (float, int))
        num_bytes = num * 1000
        return cls(num_bytes)

    @classmethod
    def from_MB(cls, num: float):
        check_typing(num, (float, int))
        num_bytes = num * 1000000
        return cls(num_bytes)

    @classmethod
    def from_GB(cls, num: float):
        check_typing(num, (float, int))
        num_bytes = num * 1000000000
        return cls(num_bytes)

    @classmethod
    def from_TB(cls, num: float):
        check_typing(num, (float, int))
        num_bytes = num * 1000000000000
        return cls(num_bytes)

    @classmethod
    def from_PB(cls, num: float):
        check_typing(num, (float, int))
        num_bytes = num * 1000000000000000
        return cls(num_bytes)


@dataclass
class RPM(Range):
    """Dataclass that stores RPM data for computer parts."""


@dataclass
class Decibels(Range):
    """Dataclass that stores decibel data for computer parts."""


@dataclass
class CFM(Range):
    """Dataclass that stores airflow data for computer parts."""


@dataclass
class FrequencyResponse(Range):
    """Dataclass that stores frequency response data for computer parts."""


@dataclass
class ClockSpeed:
    """Dataclass that stores clock speed data for various parts."""
    _cycles: int
    """int: The total number of clock cycles per second."""

    def __post_init__(self):
        check_typing(self.cycles, int)

    @property
    def cycles(self):
        return self._cycles

    @property
    def MHz(self):
        return self._cycles / 1000000.0

    @property
    def GHz(self):
        return self._cycles / 1000000000.0

    @classmethod
    def from_GHz(cls, num: float):
        check_typing(num, (float, int))
        return cls(int(num * 1000000000))

    @classmethod
    def from_MHz(cls, num: float):
        check_typing(num, (float, int))
        return cls(int(num * 1000000))


@dataclass
class NetworkSpeed:
    """Dataclass that stores network speed data."""
    _bits_per_second: int
    """int: The total number of bits per second."""

    def __post_init__(self):
        check_typing(self._bits_per_second, int)

    @property
    def bits_per_second(self):
        return self._bits_per_second

    @property
    def Mbits(self):
        return self._bits_per_second / 1000000.0

    @property
    def Gbits(self):
        return self._bits_per_second / 1000000000.0

    @classmethod
    def from_Gbits(cls, num: float):
        check_typing(num, (float, int))
        return cls(int(num * 1000000000))

    @classmethod
    def from_Mbits(cls, num: float):
        check_typing(num, (float, int))
        return cls(int(num * 1000000))




@dataclass
class CPU(Part):
    """CPU dataclass."""
    _clock_speed: ClockSpeed
    """Clockspeed: The clock speed of this CPU (in GHz)."""
    _cores: int
    """int: The number of cores that this CPU has (excludes hyperthreading + SMT)."""
    _tdp: int
    """int: The TDP of this CPU."""
    _price: Decimal
    """Decimal: The price of the CPU."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.cores, int)
        check_typing(self.tdp, int)
        check_typing(self.clock_speed, ClockSpeed)
        check_typing(self.price, Decimal)

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
class CPUCooler(Part):
    """CPU Cooler dataclass."""
    _fan_rpm: RPM
    """RPM: The RPM information of this CPU cooler."""
    _decibels: Decibels
    """Decibels: The decibel information of this CPU cooler."""
    _price: Decimal
    """Decimal: The price of the CPU cooler."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.fan_rpm, RPM)
        check_typing(self.decibels, Decibels)

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
class Motherboard(Part):
    """Motherboard dataclass."""
    _socket: str
    """str: The CPU socket type on this motherboard"""
    _form_factor: str
    """str: The form factor of this motherboard"""
    _ram_slots: int
    """int: The number of RAM slots on this motherboard"""
    _max_ram: Bytes
    """Bytes: The maximum amount of RAM that this motherboard supports (given in GB)"""
    _price: Decimal
    """Decimal: The price of this motherboard."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.socket, str)
        check_typing(self.form_factor, str)
        check_typing(self.ram_slots, int)
        check_typing(self.max_ram, Bytes)

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
class Memory(Part):
    """Memory dataclass."""
    _module_speed_data: str
    """str: The raw speed data for this module."""
    _module_type: str
    """str: The module type of this memory module"""
    _cas_timing: int
    """int: The CAS timing of this memory module"""
    _module_data: str
    """int: The number of modules and the amount of memory that these modules contain in this configuration."""
    _total_size: Bytes
    """Bytes: The total size of the modules combined."""
    _price_per_gb: float
    """float: The price per GB for this memory configuration"""
    _price: Decimal
    """Decimal: The price of this memory module."""
    _type: str = field(init=False)
    """str: The type of this memory module"""
    _speed: ClockSpeed = field(init=False)
    """ClockSpeed: The operating frequency of this memory module."""
    _number_of_modules: int = field(init=False)
    """int: The number of modules in this memory configuration."""
    _module_size: Bytes = field(init=False)
    """Bytes: The size of the modules that come with this memory configuration"""


    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self._module_speed_data, str)
        check_typing(self._module_type, str)
        check_typing(self._module_data, str)
        check_typing(self.cas_timing, int)
        check_typing(self.total_size, Bytes)
        check_typing(self.price_per_gb, float)
        self._determine_type()
        self._determine_speed()
        self._determine_module_number()
        self._determine_module_size()

    def _determine_type(self):
        self._module_speed_data = self._module_speed_data.strip()
        hyphen = self._module_speed_data.find("-")
        if not hyphen == -1 and not [x for x in self._module_speed_data if x.isnumeric()]:
            self._type = self._module_speed_data
        else:
            memory_type = [x for x in self._module_speed_data[:hyphen]]
        self._type = "".join(memory_type)

    def _determine_speed(self):
        hyphen = self._module_speed_data.find("-")
        if hyphen == -1:
            speed_data = [x for x in self._module_speed_data if x.isnumeric()]
            if speed_data:
                self._speed = ClockSpeed.from_MHz(int("".join(speed_data)))
            else:
                self._speed = None
        else:
            speed_data = [x for x in self._module_speed_data[hyphen:] if x.isnumeric()]
            self._speed = ClockSpeed.from_MHz(int("".join(speed_data)))

    def _determine_module_number(self):
        self._number_of_modules = int(self._module_data.strip()[0])

    def _determine_module_size(self):
        size = int("".join([x for x in self._module_data.strip()[2:] if x.isnumeric()]))
        if "GB" in self._module_data:
            self._module_size = Bytes.from_GB(size)
        else:
            self._module_size = Bytes.from_MB(size)

    @property
    def type(self):
        return self._type

    @property
    def speed(self):
        return self._speed

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
    def total_size(self):
        return self._total_size

    @property
    def price_per_gb(self):
        return self._price_per_gb

    @property
    def price(self):
        return self._price


@dataclass
class StorageDrive(Part):
    """Dataclass for storage devices."""
    _model_line: str
    """str: The model line of this storage device."""
    _form_factor: str
    """str: The form factor of this storage device."""
    _model_data: str
    """str: The raw data about the type of this storage device."""
    _capacity: Bytes
    """Bytes: The capacity of this storage device."""
    _cache_amount: Bytes
    """Bytes: The cache amount found in this storage device."""
    _price: Decimal
    """Decimal: The price of this storage device."""
    _type: str = field(init=False)
    """str: The type of the storage device."""
    _platter_rpm: int = field(init=False)

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.model_line, str)
        check_typing(self.form_factor, str)
        check_typing(self.capacity, Bytes)
        check_typing(self.cache_amount, Bytes)
        self._determine_type()
        self._retrieve_platter_rpm()

    def _determine_type(self):
        if [x for x in self._model_data if x.isnumeric()]:
            self._type = "HDD"
        self._type = self._model_data

    def _retrieve_platter_rpm(self):
        nums = [x for x in self._model_data if x.isnumeric()]
        if nums:
            self._platter_rpm = int("".join(nums))
        else:
            self._platter_rpm = None

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

    @property
    def type(self):
        return self._type

    @property
    def platter_rpm(self):
        return self._platter_rpm


@dataclass
class GPU(Part):
    """GPU dataclass."""
    _model_line: str
    """str: The model line of this GPU."""
    _chipset: str
    """str: The chipset of this GPU."""
    _memory_amount: Bytes
    """Bytes: The amount of video memory in this GPU."""
    _core_clock: ClockSpeed
    """ClockSpeed: The clock speed of this GPU """
    _price: Decimal
    """Decimal: The price of this GPU."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.model_line, str)
        check_typing(self.chipset, str)
        check_typing(self.memory_amount, Bytes)
        check_typing(self.core_clock, ClockSpeed)

    @property
    def model_line(self):
        return self._model_line

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
class PSU(Part):
    """PSU dataclass."""
    _model_line: str
    """str: The model line of this PSU."""
    _form_factor: str
    """str: The form factor of this PSU."""
    _efficiency_rating: str
    """str: The efficiency rating of this PSU."""
    _watt_rating: int
    """int: The watt rating of this PSU."""
    _modular: str
    """str: The modular properties of this PSU."""
    _price: Decimal
    """Decimal: The price of this PSU."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.model_line, str)
        check_typing(self.form_factor, str)
        check_typing(self.efficiency_rating, str)
        check_typing(self.watt_rating, int)
        check_typing(self.modular, str)

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
class Case(Part):
    """PC case dataclass."""
    _form_factor: str
    """str: The form factor of this case."""
    _external_bays: int
    """int: The number of external 5.25" bays in this case."""
    _internal_bays: int
    """int: The number of internal 3.5" bays in this case."""
    _psu_wattage: int
    """int: The wattage amount of the internal PSU of this case.
            If no PSU is present, this value will be set to None."""
    _price: Decimal
    """Decimal: The price of this GPU."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.form_factor, str)
        check_typing(self.external_bays, int)
        check_typing(self.internal_bays, int)
        check_typing(self.psu_wattage, int)

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
    def psu_wattage(self):
        return self._psu_wattage

    @property
    def price(self):
        return self._price


@dataclass
class Fan(Part):
    """CPU and case fan dataclass."""
    _color: str
    """str: The color of this fan."""
    _size: int
    """int: The size of this fan in millimeters."""
    _rpm: RPM
    """RPM: The RPM or RPM range of this fan."""
    _airflow: CFM
    """CFM: The amount of airflow that this fan can produce."""
    _decibels: Decibels
    """Decibels: The decibel amount or range produced by this fan."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.color, str)
        check_typing(self.size, int)
        check_typing(self.rpm, RPM)
        check_typing(self.airflow, CFM)
        check_typing(self.decibels, Decibels)

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
class FanController(Part):
    """Fan controller dataclass."""
    _form_factor: str
    """str: The form factor of this fan controller."""
    _channels: int
    """int: The number of fans that this fan controller can control."""
    _channel_wattage: int
    """int: The number of watts that this fan can provide to each channel."""
    _price: Decimal
    """Decimal: The price of this fan controller."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.form_factor, str)
        check_typing(self.channels, int)
        check_typing(self.channel_wattage, int)

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
class ThermalPaste(Part):
    """Thermal paste dataclass."""
    _amount: float
    """float: The amount of thermal paste provided in this product (in grams)."""
    _price: Decimal
    """Decimal: The price of this thermal paste."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.amount, (float, int))

    @property
    def amount(self):
        return self._amount

    @property
    def price(self):
        return self._price


@dataclass
class OpticalDrive(Part):
    """Optical drive dataclass."""
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

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.bluray_read_speed, int)
        check_typing(self.dvd_read_speed, int)
        check_typing(self.cd_read_speed, int)
        check_typing(self.bluray_write_speed, str)
        check_typing(self.dvd_write_speed, str)
        check_typing(self.cd_write_speed, str)

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
class SoundCard(Part):
    """Sound card dataclass."""
    _chipset: str
    """str: The chipset of this sound card."""
    _channels: float
    """float: The channels provided by this sound card."""
    _bitrate: int
    """int: The bitrate of this sound card."""
    _snr: int
    """int: The signal to noise ratio of this sound card in dB."""
    _sample_rate: int
    """int: The sample rate of this sound card in kHz."""
    _price: Decimal
    """Decimal: The price of this sound card."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.chipset, str)
        check_typing(self.channels, (float, int))
        check_typing(self.bitrate, int)
        check_typing(self.snr, int)
        check_typing(self.sample_rate, int)

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

    @property
    def price(self):
        return self._price


@dataclass
class EthernetCard(Part):
    """Ethernet card dataclass."""
    _interface: str
    """str: The motherboard interface of this Ethernet card."""
    _port_speed: NetworkSpeed
    """NetworkSpeed: The maximum speed that this Ethernet card supports."""
    _port_number: int
    """int: The number of Ethernet ports on this card."""
    _price: Decimal
    """Decimal: The price of this Ethernet card."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.interface, str)
        check_typing(self.port_speed, NetworkSpeed)
        check_typing(self.port_number, int)

    @property
    def interface(self):
        return self._interface

    @property
    def port_speed(self):
        return self._port_speed

    @property
    def port_number(self):
        return self._port_number

    @property
    def price(self):
        return self._price


@dataclass
class WirelessCard(Part):
    """Wireless card dataclass."""
    _interface: str
    """str: The motherboard interface of this wireless card."""
    _supported_protocols: str
    """str: The supported wireless protocols of this card."""
    _price: Decimal
    """Decimal: The price of this wireless card."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.interface, str)
        check_typing(self.supported_protocols, str)

    @property
    def interface(self):
        return self._interface

    @property
    def supported_protocols(self):
        return self._supported_protocols

    @property
    def price(self):
        return self._price


@dataclass
class Monitor(Part):
    """Monitor dataclass."""
    _resolution: Resolution
    """Resolution: The pixel dimensions of this monitor."""
    _size: float
    """float: The diagonal display size of this monitor in inches."""
    _response_time: int
    """int: The response time of this display (in milliseconds)."""
    _ips: bool
    """bool: Returns True if the panel is an IPS display."""
    _price: Decimal
    """Decimal: The price of this monitor."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.resolution, Resolution)
        check_typing(self.size, (float, int))
        check_typing(self.response_time, int)
        check_typing(self.ips, bool)

    @property
    def resolution(self):
        return self._resolution

    @property
    def size(self):
        return self._size

    @property
    def response_time(self):
        return self._response_time

    @property
    def ips(self):
        return self._ips

    @property
    def price(self):
        return self._price


@dataclass
class ExternalHDD(Part):
    """External HDD dataclass."""
    _model: str
    """str: The model line of this external HDD."""
    _type: str
    """str: The type of this external HDD."""
    _capacity: Bytes
    """Bytes: The capacity of this external HDD."""
    _price_per_gb: float
    """float: The price per GB of storage of this external HDD."""
    _price: Decimal
    """Decimal: The price of this external HDD."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.model, str)
        check_typing(self.type, str)
        check_typing(self.capacity, Bytes)
        check_typing(self.price_per_gb, (float, int))

    @property
    def model(self):
        return self._model

    @property
    def type(self):
        return self._type

    @property
    def capacity(self):
        return self._capacity

    @property
    def price_per_gb(self):
        return self._price_per_gb

    @property
    def price(self):
        return self._price


@dataclass
class Headphones(Part):
    """Headphones dataclass."""
    _type: str
    """str: The type of this set of headphones."""
    _has_microphone: bool
    """bool: Returns True if this set of headphones has a microphone."""
    _is_wireless: bool
    """bool: Returns True if this set of headphones is wireless."""
    _frequency_response: FrequencyResponse
    """str: The frequency response of this set of headphones."""
    _price: Decimal
    """Decimal: The price of these headphones."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.type, str)
        check_typing(self.has_microphone, bool)
        check_typing(self.is_wireless, bool)
        check_typing(self.frequency_response, FrequencyResponse)

    @property
    def type(self):
        return self._type

    @property
    def has_microphone(self):
        return self._has_microphone

    @property
    def is_wireless(self):
        return self._is_wireless

    @property
    def frequency_response(self):
        return self._frequency_response

    @property
    def price(self):
        return self._price


@dataclass
class Keyboard(Part):
    """Keyboard dataclass."""
    _style: str
    """str: Describes the style of this keyboard."""
    _color: str
    """str: Describes the color of this keyboard."""
    _switch_type: str
    """str: Describes the type of switches that this keyboard uses."""
    _backlight_type: str
    """str: Describes the available backlight on this device."""
    _price: Decimal
    """Decimal: The price of this keyboard."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.style, str)
        check_typing(self.color, str)
        check_typing(self.switch_type, str)
        check_typing(self.backlight_type, str)

    @property
    def style(self):
        return self._style

    @property
    def color(self):
        return self._color

    @property
    def switch_type(self):
        return self._switch_type

    @property
    def backlight_type(self):
        return self._backlight_type

    @property
    def price(self):
        return self._price


@dataclass
class Mouse(Part):
    """Computer mouse dataclass."""
    _type: str
    """str: Describes the type of this mouse."""
    _connection: str
    """str: Describes the type of connection that this mouse uses."""
    _color: str
    """str: Describes the color of this mouse."""
    _price: Decimal
    """Decimal: The price of this mouse."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.type, str)
        check_typing(self.connection, str)
        check_typing(self.color, str)

    @property
    def type(self):
        return self._type

    @property
    def connection(self):
        return self._connection

    @property
    def color(self):
        return self._color

    @property
    def price(self):
        return self._price


@dataclass
class Speakers(Part):
    """Computer speakers dataclass."""
    _channel_configuration: float
    """float: The channel configuration of this set of computer speakers."""
    _wattage: int
    """int: The peak wattage of these speakers."""
    _frequency_response: FrequencyResponse
    """FrequencyResponse: The frequency response of these speakers."""
    _price: Decimal
    """Decimal: The price of these speakers."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.channel_configuration, (float, int))
        check_typing(self.wattage, int)
        check_typing(self.frequency_response, FrequencyResponse)

    @property
    def channel_configuration(self):
        return self._channel_configuration

    @property
    def wattage(self):
        return self._wattage

    @property
    def frequency_response(self):
        return self._frequency_response

    @property
    def price(self):
        return self._price


@dataclass
class UPS(Part):
    """UPS dataclass."""
    _watt_capacity: int
    """int: The number of watts that this UPS can store."""
    _va_capacity: int
    """int: The number of volt-amperes that this UPS can store."""
    _price: Decimal
    """Decimal: The price of this UPS."""

    def __post_init__(self):
        check_typing(self.name, str)
        check_typing(self.price, Decimal)
        check_typing(self.watt_capacity, int)
        check_typing(self.va_capacity, int)

    @property
    def watt_capacity(self):
        return self._watt_capacity

    @property
    def va_capacity(self):
        return self._va_capacity

    @property
    def price(self):
        return self._price