from logger import create_logger
import logging
import unittest


class TestCreateLogger(unittest.TestCase):
    def test_logger_name(self):
        """
        Test that the passed name gets assigned
        """
        log = create_logger(__name__)
        self.assertEqual(log.name, __name__)

    def test_logger_logs(self):
        """
        Test that at least one message is logged on the logger or one of its children, with at least the given level
        """
        log = create_logger(__name__)
        with self.assertLogs(log, logging.DEBUG) as cm:
            log.debug('debug message')
            log.warning('warning message')
            log.error('error message')
        self.assertEqual(cm.output, [f'DEBUG:{log.name}:debug message',
                                     f'WARNING:{log.name}:warning message',
                                     f'ERROR:{log.name}:error message'])


if __name__ == '__main__':
    unittest.main()
