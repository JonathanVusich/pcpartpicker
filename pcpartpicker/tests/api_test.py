import pytest
import time
from pcpartpicker import API
from pcpartpicker.errors import UnsupportedRegion


# Ensure that API is initialized with the correct data
def test_api_default_init():
    api = API()
    assert api.region == "us"
    assert api.supported_parts == {"cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                        "video-card", "power-supply", "case", "case-fan", "fan-controller",
                        "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                        "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                        "keyboard", "mouse", "speakers", "ups"}

    assert api.supported_regions == {"au", "be", "ca", "de", "es", "fr", "se",
                            "in", "ie", "it", "nz", "uk", "us"}

    assert api.region == 'us'


# Ensure that API can be initialized with a different region
def test_api_region_init():
    api = API('de')
    assert api.region == 'de'


# Ensure that API throws the correct error if an incorrect region is input
def test_api_init_exception():
    with pytest.raises(UnsupportedRegion) as excinfo:
        api = API('oc')
    assert 'Region \'oc\' is not supported for this API!' in str(excinfo.value)


# Check that API.set_region works correctly
def test_api_set_region():
    api = API()
    assert(api.region == 'us')
    api.set_region('nz')
    assert(api.region == 'nz')


# Ensure that API.set_region can handle incorrect input
def test_api_set_region_incorrect_region():
    with pytest.raises(UnsupportedRegion) as excinfo:
        api = API()
        api.set_region('oc')
    assert 'Region \'oc\' is not supported for this API!' in str(excinfo)


# Check that parts are cached
def test_api_check_single_part_caching():
    api = API()
    results = api.retrieve("cpu")
    start = time.time()
    results = api.retrieve("cpu")
    if not time.time() - start < .1:
        raise AssertionError


def test_supported_parts_us():
    api = API("us")
    results = api.retrieve_all()
    for part, part_class in api._handler._parser._part_class_mappings.items():
        if part not in results:
            raise AssertionError
        failures = [item for item in results[part] if not item]
        if failures:
            raise AssertionError


def test_supported_parts_australia():
    api = API("au")
    results = api.retrieve_all()
    for part, part_class in api._handler._parser._part_class_mappings.items():
        if part not in results:
            raise AssertionError
        failures = [item for item in results[part] if not item]
        if failures:
            raise AssertionError


def test_supported_parts_canada():
    api = API("ca")
    results = api.retrieve_all()
    for part, part_class in api._handler._parser._part_class_mappings.items():
        if part not in results:
            raise AssertionError
        failures = [item for item in results[part] if not item]
        if failures:
            raise AssertionError


def test_supported_parts_europe():
    api = API("be")
    results = api.retrieve_all()
    for part, part_class in api._handler._parser._part_class_mappings.items():
        if part not in results:
            raise AssertionError
        failures = [item for item in results[part] if not item]
        if failures:
            raise AssertionError


def test_supported_parts_sweden():
    api = API("se")
    results = api.retrieve_all()
    for part, part_class in api._handler._parser._part_class_mappings.items():
        if part not in results:
            raise AssertionError
        failures = [item for item in results[part] if not item]
        if failures:
            raise AssertionError


def test_supported_parts_india():
    api = API("in")
    results = api.retrieve_all()
    for part, part_class in api._handler._parser._part_class_mappings.items():
        if part not in results:
            raise AssertionError
        failures = [item for item in results[part] if not item]
        if failures:
            raise AssertionError


def test_supported_parts_new_zealand():
    api = API("nz")
    results = api.retrieve_all()
    for part, part_class in api._handler._parser._part_class_mappings.items():
        if part not in results:
            raise AssertionError
        failures = [item for item in results[part] if not item]
        if failures:
            raise AssertionError


def test_supported_parts_uk():
    api = API("uk")
    results = api.retrieve_all()
    for part, part_class in api._handler._parser._part_class_mappings.items():
        if part not in results:
            raise AssertionError
        failures = [item for item in results[part] if not item]
        if failures:
            raise AssertionError
