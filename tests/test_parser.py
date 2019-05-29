from pcpartpicker import API
from pcpartpicker.scraper import Scraper
from pcpartpicker.parse_utils import parse
from pcpartpicker.mappings import part_classes

import asyncio
import unittest


class ParserTest(unittest.TestCase):

    @classmethod
    def parserTest(cls):
        base_api = API()
        cls.test_data = {}
        for region in base_api.supported_regions:
            api = API(region)
            cls.test_data.update({region: api.retrieve_all()})

    def test_us_tokens(self):
        results = API("us").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_uk_tokens(self):
        results = API("uk").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_nz_tokens(self):
        results = API("nz").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_it_tokens(self):
        results = API("it").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_ie_tokens(self):
        results = API("ie").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_in_tokens(self):
        results = API("in").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_se_tokens(self):
        results = API("se").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_fr_tokens(self):
        results = API("fr").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_es_tokens(self):
        results = API("es").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_de_tokens(self):
        results = API("de").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_ca_tokens(self):
        results = API("ca").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_be_tokens(self):
        results = API("be").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)

    def test_au_tokens(self):
        results = API("au").retrieve_all()
        for part, part_data in results.items():
            for p in part_data:
                self.assertIsInstance(p, part_classes[part])
                self.assertIsNotNone(p.brand)
