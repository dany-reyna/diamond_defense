from is_root import is_root
import unittest


class TestIsRoot(unittest.TestCase):
    def test_is_root(self):
        """
        Test that it can return True when the user has root permissions
        """
        self.assertTrue(is_root())


if __name__ == '__main__':
    unittest.main()
