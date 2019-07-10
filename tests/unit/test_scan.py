from scan import Host, scan
import unittest


class TestScan(unittest.TestCase):
    def test_host_scan(self):
        """
        Test that it can scan a single host
        """
        ip = '192.168.1.1'
        hosts = scan(ip)
        self.assertEqual(hosts[0].ip, ip)

    def test_network_scan(self):
        """
        Test that it can scan a network
        """
        ip = '192.168.1.0/24'
        hosts = scan(ip)
        for host in hosts:
            self.assertIsInstance(host, Host)

    def test_bad_ip(self):
        """
        Test that it returns an empty list when scanning an invalid IP
        """
        ip = '192.168.1.500'
        hosts = scan(ip)
        self.assertFalse(hosts)


if __name__ == '__main__':
    unittest.main()
