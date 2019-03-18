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
        self.assertEqual(api.concurrent_connections, 25)
        self.assertTrue(api.multithreading)

    # Ensure that API can be initialized with a different region
    def test_api_region_init(self):
        api = API('de')
        self.assertEqual(api.region, 'de')

    # Ensure that API throws the correct error if an incorrect region is input
    def test_api_init_exception(self):
        with self.assertRaises(UnsupportedRegion) as excinfo:
            api = API('oc')
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

    def test_api_concurrent_connections_kwd(self):
        api = API(concurrent_connections=100)
        self.assertEqual(api.concurrent_connections, 100)
        self.assertEqual(api._handler.concurrent_connections, 100)
        self.assertEqual(api._handler._scraper._concurrent_connections, 100)

    def test_api_modify_concurrent_connections(self):
        api = API()
        self.assertEqual(api.concurrent_connections, 25)
        self.assertEqual(api._handler.concurrent_connections, 25)
        self.assertEqual(api._handler._scraper._concurrent_connections, 25)
        api.set_concurrent_connections(100)
        self.assertEqual(api.concurrent_connections, 100)
        self.assertEqual(api._handler.concurrent_connections, 100)
        self.assertEqual(api._handler._scraper._concurrent_connections, 100)
        api.set_concurrent_connections(50)
        self.assertEqual(api.concurrent_connections, 50)
        self.assertEqual(api._handler.concurrent_connections, 50)
        self.assertEqual(api._handler._scraper._concurrent_connections, 50)

    def test_api_multithreading_kwd(self):
        api = API(multithreading=False)
        self.assertFalse(api.multithreading)
        self.assertFalse(api._handler.multithreading)

    def test_api_modify_multithreading(self):
        api = API()
        self.assertTrue(api.multithreading)
        self.assertTrue(api._handler._multithreading)
        api.set_multithreading(False)
        self.assertFalse(api._handler._multithreading)
        self.assertFalse(api.multithreading)
        api.set_multithreading(True)
        self.assertTrue(api.multithreading)
        self.assertTrue(api._handler._multithreading)


