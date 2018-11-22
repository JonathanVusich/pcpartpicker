import pytest
from pcpartpicker import API
from pcpartpicker.errors import UnsupportedRegion


# Ensure that API is initialized with the correct data
def test_api_default_init():
    api = API()
    assert api.region == "us"
    assert api.supported_parts == ["cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                        "video-card", "power-supply", "case", "case-fan", "fan-controller",
                        "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                        "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                        "keyboard", "mouse", "speakers", "ups"]
    assert api.regions == ["au", "be", "ca", "de", "es", "fr", "se",
                            "in", "ie", "it", "nz", "uk", "us"]
    assert api._parser._region == 'us'
    assert api._scraper._region == 'us'

# Ensure that API can be initialized with a different region
def test_api_region_init():
    api = API('de')
    assert api.region == 'de'
    assert api._scraper._region == 'de'
    assert api._parser._region == 'de'
    assert api._parser._currency_sign == '€'


# Ensure that API throws the correct error if an incorrect region is input
def test_api_init_exception():
    with pytest.raises(UnsupportedRegion) as excinfo:
        api = API('oc')
    assert 'Region \'oc\' is not supported!' in str(excinfo.value)


# Check that API.set_region works correctly
def test_api_set_region():
    api = API()
    assert(api.region == 'us')
    api.set_region('nz')
    assert(api.region == 'nz')
    assert api._scraper._region == 'nz'
    assert api._parser._region == 'nz'
    assert api._parser._currency_sign == '$'


# Ensure that API.set_region can handle incorrect input
def test_api_set_region_incorrect_region():
    with pytest.raises(UnsupportedRegion) as excinfo:
        api = API()
        api.set_region('oc')
    assert 'Region \'oc\' is not supported!' in str(excinfo)
