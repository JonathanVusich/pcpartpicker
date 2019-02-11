from pcpartpicker.handler import Handler
from pcpartpicker.scraper import Scraper
from pcpartpicker.parser import Parser, tokenize, html_to_tokens
from pcpartpicker.mappings import part_classes

import asyncio
import unittest


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_data = {}

        handler = Handler()
        scraper = Scraper()
        loop = asyncio.get_event_loop()
        for region in handler._regions:
            scraper.set_region(region)
            results = loop.run_until_complete(scraper.retrieve(25, *handler._supported_parts))
            region_data = dict((x, (x, y)) for x, y in zip(handler._supported_parts, results))
            cls.test_data.update({region: region_data})

    def test_us_tokens(self):
        parser = Parser()
        data = self.test_data["us"]
        parser.set_region("us")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_uk_tokens(self):
        parser = Parser()
        data = self.test_data["uk"]
        parser.set_region("uk")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_nz_tokens(self):
        parser = Parser()
        data = self.test_data["nz"]
        parser.set_region("nz")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_it_tokens(self):
        parser = Parser()
        data = self.test_data["it"]
        parser.set_region("it")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_ie_tokens(self):
        parser = Parser()
        data = self.test_data["ie"]
        parser.set_region("ie")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_in_tokens(self):
        parser = Parser()
        data = self.test_data["in"]
        parser.set_region("in")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_se_tokens(self):
        parser = Parser()
        data = self.test_data["se"]
        parser.set_region("se")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_fr_tokens(self):
        parser = Parser()
        data = self.test_data["fr"]
        parser.set_region("fr")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_es_tokens(self):
        parser = Parser()
        data = self.test_data["es"]
        parser.set_region("es")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_de_tokens(self):
        parser = Parser()
        data = self.test_data["de"]
        parser.set_region("de")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_ca_tokens(self):
        parser = Parser()
        data = self.test_data["ca"]
        parser.set_region("ca")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_be_tokens(self):
        parser = Parser()
        data = self.test_data["be"]
        parser.set_region("be")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])

    def test_au_tokens(self):
        parser = Parser()
        data = self.test_data["au"]
        parser.set_region("au")
        for part in data.keys():
            part_id, tags = html_to_tokens(data[part])
            for page in tags:
                for token in tokenize(part, page):
                    with self.subTest(part=part, token=token):
                        product = parser._parse_token(part, token)
                        self.assertIsInstance(product, part_classes[part])
