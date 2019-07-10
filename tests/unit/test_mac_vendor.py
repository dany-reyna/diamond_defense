from mac_vendor import get_vendor
import unittest


class TestGetVendor(unittest.TestCase):
    def test_good_mac(self):
        """
        Test that it returns the vendor from a given mac
        """
        mac = '08:74:02:00:00:00'
        vendor = get_vendor(mac)
        self.assertEqual(vendor, 'Apple, Inc.')

    def test_empty_mac(self):
        """
        Test that it returns the specified message when the mac is empty
        """
        mac = ''
        vendor = get_vendor(mac)
        self.assertEqual(vendor, 'Please provide mac address')

    def test_bad_mac(self):
        """
        Test that it returns the specified message when the mac is not correct
        """
        mac = '12:13:14:00:00:45'
        vendor = get_vendor(mac)
        self.assertEqual(vendor, 'No vendor')


if __name__ == '__main__':
    unittest.main()
