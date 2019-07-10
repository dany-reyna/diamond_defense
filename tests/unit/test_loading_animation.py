from loading_animation import LoadingThread
import time
import unittest


class TestLoadingAnimation(unittest.TestCase):
    def test_start(self):
        """
        Test that it can start the animation thread
        """
        animation = LoadingThread('message')
        animation.start()
        self.assertTrue(animation.is_alive())
        animation.stop()

    def test_stop(self):
        """
        Test that it can stop the animation thread
        """
        animation = LoadingThread('message')
        animation.start()
        animation.stop()
        time.sleep(0.5)
        self.assertFalse(animation.is_alive())


if __name__ == '__main__':
    unittest.main()
