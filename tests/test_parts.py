import unittest

from pcpartpicker.parts import check_typing, Bytes, Resolution, ClockSpeed, Decibels, RPM, CFM, NetworkSpeed


class PartTest(unittest.TestCase):

    def test_check_typing(self):
        self.assertIsNone(check_typing(12, int))
        with self.assertRaises(ValueError):
            check_typing(12.3, int)
        self.assertIsNone(check_typing(None, int))

    def test_bytes_init(self):
        size = Bytes(50)
        self.assertEqual(size.total, 50)
        self.assertEqual(size.kb, 0.05)
        self.assertEqual(size.mb, 0.00005)
        self.assertEqual(size.gb, 0.00000005)
        self.assertEqual(size.tb, 0.00000000005)
        self.assertEqual(size.pb, 0.00000000000005)

    def test_bytes_bad_init(self):
        with self.assertRaises(ValueError):
            _ = Bytes("50")

    def test_bytes_from_kb(self):
        size = Bytes.from_kb(50)
        self.assertEqual(size.total, 50000)
        self.assertEqual(size.kb, 50)
        self.assertEqual(size.mb, 0.05)
        self.assertEqual(size.gb, 0.00005)
        self.assertEqual(size.tb, 0.00000005)
        self.assertEqual(size.pb, 0.00000000005)

    def test_bytes_from_mb(self):
        size = Bytes.from_mb(50)
        self.assertEqual(size.total, 50000000)
        self.assertEqual(size.kb, 50000)
        self.assertEqual(size.mb, 50)
        self.assertEqual(size.gb, 0.05)
        self.assertEqual(size.tb, 0.00005)
        self.assertEqual(size.pb, 0.00000005)

    def test_bytes_from_gb(self):
        size = Bytes.from_gb(50)
        self.assertEqual(size.total, 50000000000)
        self.assertEqual(size.kb, 50000000)
        self.assertEqual(size.mb, 50000)
        self.assertEqual(size.gb, 50)
        self.assertEqual(size.tb, 0.05)
        self.assertEqual(size.pb, 0.00005)

    def test_bytes_from_tb(self):
        size = Bytes.from_tb(50)
        self.assertEqual(size.total, 50000000000000)
        self.assertEqual(size.kb, 50000000000)
        self.assertEqual(size.mb, 50000000)
        self.assertEqual(size.gb, 50000)
        self.assertEqual(size.tb, 50)
        self.assertEqual(size.pb, 0.05)

    def test_bytes_from_pb(self):
        size = Bytes.from_pb(50)
        self.assertEqual(size.total, 50000000000000000)
        self.assertEqual(size.kb, 50000000000000)
        self.assertEqual(size.mb, 50000000000)
        self.assertEqual(size.gb, 50000000)
        self.assertEqual(size.tb, 50000)
        self.assertEqual(size.pb, 50)

    def test_resolution_init(self):
        resolution = Resolution(1920, 1080)
        self.assertEqual(resolution.width, 1920)
        self.assertEqual(resolution.height, 1080)

    def test_resolution_bad_init(self):
        with self.assertRaises(ValueError):
            _ = Resolution("1920", "1080")

    def test_clock_speed_init(self):
        clock_speed = ClockSpeed(3450000000)
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)

    def test_clock_speed_bad_init(self):
        with self.assertRaises(ValueError):
            _ = ClockSpeed("This is a test")

    def test_clock_speed_from_GHz_float(self):
        clock_speed = ClockSpeed.from_ghz(3.45)
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)
        self.assertEqual(clock_speed.cycles, 3450000000)

    def test_clock_speed_from_GHz_str(self):
        clock_speed = ClockSpeed.from_ghz("3.45")
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)
        self.assertEqual(clock_speed.cycles, 3450000000)

    def test_clock_speed_from_GHz_bad_str(self):
        with self.assertRaises(ValueError):
            _ = ClockSpeed.from_ghz("This is a test")

    def test_clock_speed_from_MHz_float(self):
        clock_speed = ClockSpeed.from_mhz(3450)
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)
        self.assertEqual(clock_speed.cycles, 3450000000)

    def test_clock_speed_from_MHz_str(self):
        clock_speed = ClockSpeed.from_mhz("3450")
        self.assertEqual(clock_speed.mhz, 3450)
        self.assertEqual(clock_speed.ghz, 3.45)
        self.assertEqual(clock_speed.cycles, 3450000000)

    def test_clock_speed_from_MHz_bad_str(self):
        with self.assertRaises(ValueError):
            _ = ClockSpeed.from_mhz("this is a test")

    def test_decibel_init(self):
        decibels = Decibels(12.5, 34.5, 22)
        self.assertEqual(decibels.min, 12.5)
        self.assertEqual(decibels.max, 34.5)
        self.assertEqual(decibels.default, 22)

    def test_decibel_bad_init(self):
        with self.assertRaises(ValueError):
            args = ["12.5", "34.5", "23.1"]
            _ = Decibels(*args)

    def test_rpm_init(self):
        args = [12.5, 34.5, 22]
        rpm = RPM(*args)
        self.assertEqual(rpm.min, args[0])
        self.assertEqual(rpm.max, args[1])
        self.assertEqual(rpm.default, args[2])

    def test_rpm_bad_init(self):
        with self.assertRaises(ValueError):
            args = ["12.5", "34.5", "23.1"]
            _ = RPM(*args)

    def test_cfm_init(self):
        args = [12.5, 34.5, 22]
        cfm = CFM(*args)
        self.assertEqual(cfm.min, args[0])
        self.assertEqual(cfm.max, args[1])
        self.assertEqual(cfm.default, args[2])

    def test_cfm_bad_init(self):
        args = ["12.5", "34.5", "23.1"]
        with self.assertRaises(ValueError):
            _ = CFM(*args)

    def test_network_speed_init(self):
        network_speed = NetworkSpeed(2000)
        self.assertEqual(network_speed.bits_per_second, 2000)

    def test_network_speed_bad_init(self):
        with self.assertRaises(ValueError):
            _ = NetworkSpeed.from_gbits("2")

    def test_network_speed_from_mbits(self):
        network_speed = NetworkSpeed.from_mbits(1000)
        self.assertEqual(network_speed.mbits, 1000)
        self.assertEqual(network_speed.gbits, 1)

    def test_network_speed_from_gbits(self):
        network_speed = NetworkSpeed.from_gbits(2)
        self.assertEqual(network_speed.mbits, 2000)
        self.assertEqual(network_speed.gbits, 2)
