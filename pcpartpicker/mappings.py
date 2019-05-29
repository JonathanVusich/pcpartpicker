from typing import Dict, Callable

from .parts import CPU, CPUCooler, Motherboard, Memory, EthernetCard, WirelessCard, Case, \
    PSU, GPU, StorageDrive, Fan, FanController, ThermalPaste, OpticalDrive, SoundCard, \
    Monitor, ExternalHDD, Headphones, Keyboard, Mouse, Speakers, UPS

part_classes: Dict[str, Callable] = {
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
