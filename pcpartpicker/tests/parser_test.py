import unittest
from pcpartpicker.handler import Handler
from pcpartpicker.scraper import Scraper
from pcpartpicker.parser import tokenize, html_to_tokens
import json
import asyncio

from pcpartpicker.parts import CPU, CPUCooler, Motherboard, Memory, EthernetCard, WirelessCard, Case, \
    PSU, GPU, StorageDrive, Fan, FanController, ThermalPaste, OpticalDrive, SoundCard, \
    Monitor, ExternalHDD, Headphones, Keyboard, Mouse, Speakers, UPS, Bytes, ClockSpeed

from pcpartpicker.parser import Parser
from moneyed import Money, USD, INR, SEK, EUR, GBP


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._test_data = {}

        handler = Handler()
        scraper = Scraper()
        loop = asyncio.get_event_loop()
        for region in handler._regions:
            scraper._set_region(region)
            results = loop.run_until_complete(scraper._retrieve(*handler._supported_parts))
            region_data = dict((x, (x, y)) for x, y in zip(handler._supported_parts, results))
            cls._test_data.update({region: region_data})

    def test_us_cpu(self):
        parser = Parser()
        for part, data in self._test_data["us"]["cpu"]:
            cpu = parser._parse_token(part, data)
            self.assertIsInstance(cpu, CPU)

