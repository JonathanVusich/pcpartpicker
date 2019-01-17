from moneyed import USD, AUD, CAD, EUR, NZD, SEK, GBP, INR
from .parts import CPU, CPUCooler, Motherboard, Memory, EthernetCard, WirelessCard, Case, \
    PSU, GPU, StorageDrive, Fan, FanController, ThermalPaste, OpticalDrive, SoundCard, \
    Monitor, ExternalHDD, Headphones, Keyboard, Mouse, Speakers, UPS, Bytes, ClockSpeed


num_pattern = r"(?<![a-zA-Z:])[-+]?\d*\.?\d+"

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

hdd_form_factors = {"1.8\"", "2.5\"", "3.5\"", "M.2-22110", "M.2-2242",
                    "M.2-2260", "M.2-2280", "mSATA", "PCI-E"}

colors = {"Black", "Beige", "Beige / Gray", "Beige / Black", "Black / Beige", "Black / Blue", "Black / Gold",
          "Black / Gray", "Black / Green", "Black / Multicolor", "Black / Orange", "Black / Pink",
          "Black / Purple", "Black / Red", "Black / Silver", "Black / White", "Black / Yellow", "Blue",
          "Blue / Black", "Blue / Gray", "Blue / Pink", "Blue / Silver", "Blue / White", "Brown",
          "Brown / Black", "Camo", "Gold", "Dark Silver", "Gold / White", "Gray", "Gray / Black", "Gray / Blue",
          "Gray / Silver", "Gray / White", "Gray / White", "Gray / Yellow", "Green", "Green / Black",
          "Green / Blue", "Green / Silver", "Green / White", "Gunmetal", "Multicolor", "Orange",
          "Orange / Black", "Orange / White", "Pink", "Pink / Black", "Pink / White", "Purple", "Purple / Black",
          "Red", "Red / White", "Red / Black", "Red / Blue", "Red / Silver", "Silver", "Silver / Black",
          "Silver / Beige", "Silver / Black", "Silver / Blue", "Silver / Gray", "Silver / White",
          "White", "White / Black", "White / Blue", "White / Gray", "White / Purple", "White / Red",
          "White / Pink", "White / Silver", "White / Yellow", "Yellow / Black", "Yellow"}

backlights = {"No", "Yellow", "White", "Red/Blue", "Red/Amber", "Red", "Purple",
              "Orange", "Multicolor", "Green", "Blue/Silver", "Blue"}

mobo_interfaces = ["PCI", "USB"]

net_speeds = ["Mbit/s", "Gbit/s"]

byte_classes = {"GB": Bytes.from_GB, "TB": Bytes.from_TB, "MB": Bytes.from_MB,
                "KB": Bytes.from_KB, "PB": Bytes.from_PB}

wifi_protocol = ["802.11"]

cases = {"ATX Desktop", "ATX Full Tower", "ATX Mid Tower", "ATX Mini Tower", "ATX Test Bench", "HTPC",
         "MicroATX Desktop", "MicroATX Mid Tower", "MicroATX Mini Tower", "MicroATX Slim",
         "Mini ITX Desktop", "Mini ITX Test Bench", "Mini ITX Tower"}

bitrates = {"24", "16"}

psu_form_factors = {"ATX", "SFX", "TFX", "EPS", "BTX", "Flex ATX", "Micro ATX", "Mini ITX"}

psu_modularity_options = {"No", "Semi", "Full"}

gpu_chipsets = ["GeForce ", "Radeon ", "Vega ", "Titan ", "Quadro ", "NVS ", "FirePro ", "FireGL ", "TITAN "]

currency_symbols = {"us": "$", "au": "$", "ca": "$", "be": "€", "de": "€", "es": "€", "fr": "€",
                    "ie": "€", "it": "€", "nl": "€", "nz": "$", "se": "kr", "uk": "£", "in": "₹"}

currency_classes = {"us": USD, "au": AUD, "ca": CAD, "be": EUR, "de": EUR, "es": EUR, "fr": EUR,
                    "ie": EUR, "it": EUR, "nl": EUR, "nz": NZD, "se": SEK, "uk": GBP, "in": INR}

clockspeeds = {"GHz": ClockSpeed.from_GHz, "MHz": ClockSpeed.from_MHz}

watt_symbol = [" W"]

watt_levels = [" W", " kW", " mW", " nW"]
