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


model_mappings = {
    "cpu": ["AMD", "Intel"],
    "cpu-cooler": ["AMD", "ARTIC", "Akasa", "Alpenföhn", "Alphacool", "Antec",
                   "Asus", "CRYORIG", "Cooler Master", "Cooltek", "Corsair",
                   "Deepcool", "Dynatron", "EVGA", "Enermax", "Enzotech",
                   "Evercool", "FSP Group", "Fractal Design", "Gelid Solutions",
                   "Gigabyte", "ID-COOLING", "Intel", "LEPA", "Logisys",
                   "MSI", "Masscool", "NZXT", "Nexus", "NoFan", "Noctua",
                   "OcUK", "Phanteks", "Phononic", "Prolimatech", "RAIJINTEK",
                   "RIOTORO", "ROCCAT", "Raidmax", "Reeven", "Rosewill", "Scythe",
                   "SilenX", "SilentiumPC", "Silverstone", "StarTech", "Sunbeam",
                   "Swiftech", "Syba", "TUNIQ", "Thermalright", "Thermaltake",
                   "Titan", "Vantec", "X2", "Xigmatek", "Xion", "ZEROtherm",
                   "Zalman", "Zero Infinity", "be quiet!"],
    "motherboard": ["ASRock", "Asus", "Biostar", "ECS", "EVGA", "Foxconn",
                    "Gigabyte", "Intel", "Jetway", "MSI", "NZXT", "Sapphire",
                    "Supermicro", "XFX", "Zotac"],
    "memory": ["ADATA", "AMD", "Apacer", "Apotop", "Avexir", "Compustocx",
               "Corsair", "Crucial", "Dell", "EVGA", "Edge Tech", "G.Skill",
               "GALAX", "GeIL", "Gigabyte", "Gloway", "HP", "IBM", "KFA2",
               "Kingston", "Klevv", "Lexar", "Micron", "Mushkin", "OCZ", "PNY",
               "Panram", "Pareema", "Patriot", "SK hynix", "Samsung", "Silicon Power",
               "Team", "Toshiba", "Transcend", "V-Color", "V7", "VisionTek",
               "Wintec"],
    "wired-network-card": ["Acer", "Asus", "Belkin", "Cisco", "D-Link", "Edimax",
                           "Gigabyte", "Intel", "Lenovo", "Netgear", "Plugable",
                           "QLogic", "QNAP", "Rosewill", "SIIG", "StarTech", "Supermicro",
                           "Syba", "TP-Link", "TRENDnet", "VisionTek"],
    "wireless-network-card": ["3M", "AUKEY", "AVM", "Asus", "Athenatech", "Belkin",
                              "BenQ", "Buffalo Technology", "Cisco", "D-Link",
                              "Diamond", "Edimax", "Encore", "Feb Smart", "Gigabyte",
                              "HP", "Hawking Technology", "IOGEAR", "Inamax", "Intel",
                              "Linksys", "Netgear", "Orico", "Patriot", "Rosewill",
                              "SIIG", "Samsung", "StarTech", "Syba", "TP-Link",
                              "TRENDnet", "fenvi"],
    "case": ["ABS", "Aerocool", "Anidees", "Antec", "Apevia", "Apex", "Asus",
             "Athena Power", "Athenatech", "AvP", "Azza", "BitFenix", "Broadway",
             "CFI", "CHENBRO", "CRYORIG", "Chieftec", "CiT", "Cooler Master",
             "Cooltek", "Corsair", "Cougar", "Cubitek", "DAN", "DIYPC", "Deepcool",
             "Diablotek", "Dynapower", "EVGA", "Element", "Enermax", "FSP Group",
             "Foxconn", "Fractal Design", "GAMDIAS", "Game Max", "GamerChief",
             "Gigabyte", "HEC", "HG Computers", "HP", "Inwin", "JMAX", "Jonsbo",
             "KOLINK", "LC-Power", "LDLC", "LEPA", "Lazer3D", "Lian-Li", "Linkworld",
             "Logisys", "MS-Tech", "MSI", "Mars Gaming", "Metallic Gear", "Morex",
             "NOX", "NZXT", "Nanoxia", "Parvum", "Phanteks", "PrimoChill", "Powertek",
             "RAIJINTEK", "RIOTORO", "Raidmax", "Raygo", "Rosewill", "SAMA", "SHARKOON",
             "Sahara", "Segotep", "Sentey", "Sigma", "Silverstone", "Spartex",
             "Streacom", "Sunbeam", "Supermicro", "TUNIQ", "Thermaltake", "Topower",
             "Ultra", "VIVO", "Wesena", "X2", "XClio", "XFX", "Xigmatek", "Xion",
             "Zalman", "Zodiac", "be quiet!", "darkFlash", "iBuypower", "iStarUSA",
             "mean:it", "nMEDIAPC"]

}
