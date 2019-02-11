from pcpartpicker.scraper import Scraper
from pcpartpicker.errors import UnsupportedRegion
import unittest


class ScraperTest(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper()

    def test_scraper_default_init(self):
        assert(self.scraper._region == "us")
        assert(self.scraper._base_url == "https://pcpartpicker.com/products/")

    def test_scraper_change_region(self):
        self.scraper.set_region("nz")
        self.assertEqual(self.scraper._region, "nz")
        self.assertEqual(self.scraper._base_url, "https://nz.pcpartpicker.com/products/")

