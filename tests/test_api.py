import unittest

from pcpartpicker import API
from pcpartpicker.errors import UnsupportedRegion


class APITest(unittest.TestCase):

    # Ensure that API is initialized with the correct data
    def test_api_default_init(self):
        api = API()
        self.assertEqual(api.region, "us")
        self.assertEqual(api.supported_parts, {"cpu", "cpu-cooler", "motherboard", "memory", "internal-hard-drive",
                                               "video-card", "power-supply", "case", "case-fan", "fan-controller",
                                               "thermal-paste", "optical-drive", "sound-card", "wired-network-card",
                                               "wireless-network-card", "monitor", "external-hard-drive", "headphones",
                                               "keyboard", "mouse", "speakers", "ups"})

        self.assertEqual(api.supported_regions, {"au", "be", "ca", "de", "es", "fr", "se",
                                                 "in", "ie", "it", "nz", "uk", "us"})

        self.assertEqual(api.region, 'us')

    # Ensure that API can be initialized with a different region
    def test_api_region_init(self):
        api = API('de')
        self.assertEqual(api.region, 'de')

    # Ensure that API throws the correct error if an incorrect region is input
    def test_api_init_exception(self):
        with self.assertRaises(UnsupportedRegion) as excinfo:
            _ = API('oc')
        assert 'Region \'oc\' is not supported for this API!' in str(excinfo.exception)

    # Check that API.set_region works correctly
    def test_api_set_region(self):
        api = API()
        self.assertEqual(api.region, 'us')
        api.set_region('nz')
        self.assertEqual(api.region, 'nz')

    # Ensure that API.set_region can handle incorrect input
    def test_api_set_region_incorrect_region(self):
        with self.assertRaises(UnsupportedRegion) as excinfo:
            api = API()
            api.set_region('oc')
        assert 'Region \'oc\' is not supported for this API!' in str(excinfo.exception)
