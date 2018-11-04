import pytest
from pcpartpicker.scraper import Scraper
from pcpartpicker.errors import UnsupportedRegion

# Ensure that the region defaults to "us"
def scraper_default_init_test():
    scraper = Scraper()
    assert(scraper.region == "us")
    assert(scraper._supported_types == ["cpu"])
    assert(scraper._regions == ["au", "be", "ca", "de", "es", "fr",
                    "in", "ie", "it", "nz", "uk", "us"])
    assert(scraper._region == "us")
    assert(scraper._base_url == "https://pcpartpicker.com/products/")

# Ensure that the scraper default region can be changed
def scraper_change_region_test():
    scraper = Scraper()
    scraper._set_region = "nz"
    assert(scraper.region == "nz")

def scraper_region_exception_test():
    with pytest.raises(UnsupportedRegion) as excinfo:
        scraper = Scraper()
        scraper._set_region = "oc"
    assert 'Region \'oc\' is not supported!' in str(excinfo.value)
