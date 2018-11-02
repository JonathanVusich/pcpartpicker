import pytest
from pcpartpicker import *

def test_api_default_init():
    api = API()
    assert(api.region == "us")

def test_api_region_init():
    api = API('de')
    assert(api.region == 'de')

def test_api_init_exception():
    with pytest.raises(UnsupportedRegion) as excinfo:
        api = API('oc')
    assert 'Region oc is not supported!' in str(excinfo.value)
