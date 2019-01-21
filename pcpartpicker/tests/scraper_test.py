from pcpartpicker.scraper import Scraper


# Ensure that the region defaults to "us"
def test_scraper_default_init():
    scraper = Scraper()
    assert(scraper._region == "us")
    assert(scraper._base_url == "https://pcpartpicker.com/products/")


# Ensure that the scraper default region can be changed
def test_scraper_change_region():
    scraper = Scraper()
    scraper._set_region("nz")
    assert(scraper._region == "nz")
    assert(scraper._base_url == "https://nz.pcpartpicker.com/products/")


# Ensure that the scraper throws an error if an unsupported region is attempted to be selected
def test_scraper_region_exception():
    scraper = Scraper()
    scraper._set_region("oc")
    assert scraper._region == 'oc'

