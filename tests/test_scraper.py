import unittest

from pcpartpicker.scraper import Scraper


class ScraperTest(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper()

    def test_scraper_default_init(self):
        self.assertEqual(self.scraper._region, "us")
        self.assertEqual(self.scraper._base_url, "https://pcpartpicker.com/products/")

    def test_scraper_change_region(self):
        self.scraper = Scraper("nz")
        self.assertEqual(self.scraper._region, "nz")
        self.assertEqual(self.scraper._base_url, "https://nz.pcpartpicker.com/products/")
