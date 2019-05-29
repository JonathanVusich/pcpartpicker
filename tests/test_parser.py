from pcpartpicker.handler import Handler
from pcpartpicker.scraper import Scraper
from pcpartpicker.parse_utils import parse
from pcpartpicker.mappings import part_classes

import asyncio
import unittest


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_data = {}

        handler = Handler()
        loop = asyncio.get_event_loop()
        for region in handler._supported_regions:
            scraper = Scraper(region)
            results = loop.run_until_complete(scraper.retrieve(handler._supported_parts))
            cls.test_data.update({region: results})

    def test_us_tokens(self):
        data = self.test_data["us"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)


    def test_uk_tokens(self):
        data = self.test_data["uk"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_nz_tokens(self):
        data = self.test_data["nz"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_it_tokens(self):
        data = self.test_data["it"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_ie_tokens(self):
        data = self.test_data["ie"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_in_tokens(self):
        data = self.test_data["in"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_se_tokens(self):
        data = self.test_data["se"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_fr_tokens(self):
        data = self.test_data["fr"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_es_tokens(self):
        data = self.test_data["es"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_de_tokens(self):
        data = self.test_data["de"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_ca_tokens(self):
        data = self.test_data["ca"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_be_tokens(self):
        data = self.test_data["be"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)

    def test_au_tokens(self):
        data = self.test_data["au"]
        results = parse(data)
        for part, part_data in results.items():
            for p in part_data:
                with self.subTest():
                    self.assertIsInstance(p, part_classes[part])
                    self.assertIsNotNone(p.brand)
