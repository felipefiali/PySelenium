from unittest import TestCase
from tests.testables import DriverTestable
from tests.testables import WebDriverWaitTestable
from tests.testables import WebElementStub
from _selenium_wrapper import ElementNotFoundError
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from mock import patch


class TestDriver(TestCase):
    """Has unit tests for the Driver class"""

    def test_navigate(self):
        any_url = 'http://someurl.com'

        testable_driver = DriverTestable()

        with patch.object(testable_driver.driver, 'get') as driver_mock:
            testable_driver.navigate(any_url)

            driver_mock.assert_called_with(any_url)

    def test_navigate_error(self):
        testable_driver = DriverTestable()

        self.assertRaises(ValueError, testable_driver.navigate, '')
        self.assertRaises(TypeError, testable_driver.navigate, None)

    def test_exit(self):
        testable_driver = DriverTestable()

        with patch.object(testable_driver.driver, 'close') as driver_mock:
            testable_driver.__exit__(None, None, None)
            self.assertTrue(driver_mock.called)
            self.assertIsNone(testable_driver.driver)

    def test_click(self):
        testable_driver = DriverTestable()

        web_driver_wait_testable = WebDriverWaitTestable()

        web_element_stub = WebElementStub()

        with patch.object(web_element_stub, 'click') as clicked_mock:
            with patch.object(web_element_stub, 'is_enabled') as enabled_mock:
                web_driver_wait_testable.inject_web_element_stub(web_element_stub)

                testable_driver.inject_web_driver_wait_testable(web_driver_wait_testable)

                testable_driver.click('any css path', '')

                self.assertTrue(clicked_mock.called)
                self.assertTrue(enabled_mock.called)

    def test_click_error_empty_css_path(self):
        testable_driver = DriverTestable()

        self.assertRaises(ValueError, testable_driver.click, '', '')
        self.assertRaises(ValueError, testable_driver.click, None, '')

    def test_no_such_element_error(self):
        web_driver_wait_testable = WebDriverWaitTestable()

        web_driver_wait_testable.stub_exception_to_be_raised_on_until(NoSuchElementException)

        testable_driver = DriverTestable()
        testable_driver.inject_web_driver_wait_testable(web_driver_wait_testable)

        self.assertRaises(ElementNotFoundError, testable_driver.click, 'any css path', '')

    def test_timeout_error(self):
        web_driver_wait_testable = WebDriverWaitTestable()

        web_driver_wait_testable.stub_exception_to_be_raised_on_until(TimeoutException)

        testable_driver = DriverTestable()
        testable_driver.inject_web_driver_wait_testable(web_driver_wait_testable)

        self.assertRaises(ElementNotFoundError, testable_driver.click, 'any css path', '')
