from unittest import TestCase
from tests.testables import DriverTestable
from mock import patch


class TestDriver(TestCase):
    """Has unit tests for the Driver class"""

    def test_navigate(self):
        any_url = 'http://someurl.com'

        testable_driver = DriverTestable()

        with patch.object(testable_driver.driver, 'get') as driver_mock:
            testable_driver.navigate(any_url)

            driver_mock.assert_called_with(any_url)

    def test_exit(self):
        testable_driver = DriverTestable()

        with patch.object(testable_driver.driver, 'close') as driver_mock:
            testable_driver.__exit__(None, None, None)
            self.assertTrue(driver_mock.called)
            self.assertIsNone(testable_driver.driver)
