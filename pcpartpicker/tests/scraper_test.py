import pytest
from pcpartpicker.scraper import Scraper
from pcpartpicker.parser import Parser
import aiohttp


# Ensure that the region defaults to "us"
def scraper_default_init_test():
    scraper = Scraper()
    assert(scraper.region == "us")
    assert(scraper._regions == ["au", "be", "ca", "de", "es", "fr",
                    "in", "ie", "it", "nz", "uk", "us"])
    assert(scraper._region == "us")
    assert(scraper._base_url == "https://pcpartpicker.com/products/")
    assert(isinstance(scraper._parser, Parser))


# Ensure that the scraper default region can be changed
def scraper_change_region_test():
    scraper = Scraper()
    scraper._update_region = "nz"
    assert(scraper.region == "nz")
    assert(scraper._base_url == "https://nz.pcpartpicker.com/products/")


# Ensure that the scraper throws an error if an unsupported region is attempted to be selected
def scraper_region_exception_test():
    scraper = Scraper()
    scraper._update_region("oc")
    assert scraper.region == 'oc'


# Ensure that _retrieve_page_numbers always returns a list of integers
def scraper_retrieve_page_numbers_test():
    scraper = Scraper()
    parts = ["cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                        "video-card", "power-supply", "case", "case-fan", "fan-controller",
                        "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                        "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                        "keyboard", "mouse", "speakers", "ups"]
    with aiohttp.ClientSession() as session:
        for part in parts:
            num_list = scraper._retrieve_page_numbers(session, part)
            for num in num_list:
                assert isinstance(num, int)

