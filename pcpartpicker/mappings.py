from moneyed import USD, AUD, CAD, EUR, NZD, SEK, GBP, INR
from .parts import CPU, CPUCooler, Motherboard, Memory, EthernetCard, WirelessCard, Case, \
    PSU, GPU, StorageDrive, Fan, FanController, ThermalPaste, OpticalDrive, SoundCard, \
    Monitor, ExternalHDD, Headphones, Keyboard, Mouse, Speakers, UPS, Bytes, ClockSpeed


part_classes = {
    "cpu": CPU,
    "cpu-cooler": CPUCooler,
    "motherboard": Motherboard,
    "memory": Memory,
    "wired-network-card": EthernetCard,
    "wireless-network-card": WirelessCard,
    "case": Case,
    "power-supply": PSU,
    "video-card": GPU,
    "internal-hard-drive": StorageDrive,
    "case-fan": Fan,
    "fan-controller": FanController,
    "thermal-paste": ThermalPaste,
    "optical-drive": OpticalDrive,
    "sound-card": SoundCard,
    "monitor": Monitor,
    "external-hard-drive": ExternalHDD,
    "headphones": Headphones,
    "keyboard": Keyboard,
    "mouse": Mouse,
    "speakers": Speakers,
    "ups": UPS
}

byte_classes = {"GB": Bytes.from_gb, "TB": Bytes.from_tb, "MB": Bytes.from_mb,
                "KB": Bytes.from_kb, "PB": Bytes.from_pb}

currency_symbols = {"us": "$", "au": "$", "ca": "$", "be": "€", "de": "€", "es": "€", "fr": "€",
                    "ie": "€", "it": "€", "nl": "€", "nz": "$", "se": "kr", "uk": "£", "in": "₹"}

currency_classes = {"us": USD, "au": AUD, "ca": CAD, "be": EUR, "de": EUR, "es": EUR, "fr": EUR,
                    "ie": EUR, "it": EUR, "nl": EUR, "nz": NZD, "se": SEK, "uk": GBP, "in": INR}

clockspeeds = {"GHz": ClockSpeed.from_ghz, "MHz": ClockSpeed.from_mhz}

none_symbols = {"-", "N/A", "None"}
