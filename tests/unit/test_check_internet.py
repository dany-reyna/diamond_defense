from check_internet import is_connected
import unittest


class TestIsConnected(unittest.TestCase):
    def test_connection(self):
        """
        Test that it can return True when there is internet
        """
        self.assertTrue(is_connected())

    def test_bad_url(self):
        """
        Test that it returns False when it can't open a site
        """
        self.assertFalse(is_connected(site='https://notadomaindomino.com'))


if __name__ == '__main__':
    unittest.main()
