from unittest import TestCase
from tests.testables import DriverTestable
from tests.testables import WebDriverWaitTestable
from tests.testables import WebElementStub
from tests.test_data import *
from _selenium_wrapper import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from mock import patch
from mock import PropertyMock
from mock import call


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
            with patch.object(web_element_stub, 'is_enabled'):
                web_driver_wait_testable.inject_web_element_stub(web_element_stub)

                testable_driver.inject_web_driver_wait_testable(web_driver_wait_testable)

                testable_driver.click('any css path', '')

                self.assertTrue(clicked_mock.called)

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

    def test_find_element(self):
        web_driver_wait_testable = WebDriverWaitTestable()

        with patch.object(web_driver_wait_testable, 'until') as web_driver_wait_mock:
            testable_driver = DriverTestable()
            testable_driver.inject_web_driver_wait_testable(web_driver_wait_testable)

            presence = presence_of_element_located(None)

            testable_driver.inject_presence_of_element_located(presence)

            testable_driver.find_element(ANY_CSS_PATH, ANY_HINT)

            web_driver_wait_mock.assert_called_with(presence)

    def test_find_element_no_such_element(self):
        web_driver_wait_testable = WebDriverWaitTestable()

        with patch.object(web_driver_wait_testable, 'until') as web_driver_wait_mock:
            exception = NoSuchElementException()

            web_driver_wait_mock.side_effect = exception

            testable_driver = DriverTestable()
            testable_driver.inject_web_driver_wait_testable(web_driver_wait_testable)

            try:
                testable_driver.find_element(ANY_CSS_PATH, ANY_HINT)
            except ElementNotFoundError as ex:
                self.assertEqual(ex.inner_exception, exception)
                self.assertEqual(ex.css_path, ANY_CSS_PATH)
                self.assertEqual(ex.hint, ANY_HINT)

    def test_find_element_timeout(self):
        web_driver_wait_testable = WebDriverWaitTestable()

        with patch.object(web_driver_wait_testable, 'until') as web_driver_wait_mock:
            exception = TimeoutException()

            web_driver_wait_mock.side_effect = exception

            testable_driver = DriverTestable()
            testable_driver.inject_web_driver_wait_testable(web_driver_wait_testable)

            try:
                testable_driver.find_element(ANY_CSS_PATH, ANY_HINT)
            except ElementNotFoundError as ex:
                self.assertEqual(ex.inner_exception, exception)
                self.assertEqual(ex.css_path, ANY_CSS_PATH)
                self.assertEqual(ex.hint, ANY_HINT)

    def test_find_element_css_path_empty(self):
        driver_testable = DriverTestable()

        self.assertRaises(ValueError, driver_testable.find_element, '', ANY_HINT)
        self.assertRaises(ValueError, driver_testable.find_element, None, ANY_HINT)

    def test_get_attribute_value(self):
        testable_driver = DriverTestable()
        element_stub = WebElementStub()

        with patch.object(testable_driver, 'find_element', return_value=element_stub) as find_element_mock:
            with patch.object(element_stub, 'get_attribute', return_value=ANY_VALUE) as element_mock:
                returned_value = testable_driver.get_element_attribute(ANY_CSS_PATH, ANY_HINT, ANY_ATTRIBUTE_NAME)

                self.assertEqual(returned_value, ANY_VALUE)

                find_element_mock.assert_called_with(ANY_CSS_PATH, ANY_HINT)
                element_mock.assert_called_with(ANY_ATTRIBUTE_NAME)

    def test_get_attribute_empty_args(self):
        testable_driver = DriverTestable()

        self.assertRaises(ValueError, testable_driver.get_element_attribute, None, ANY_HINT, ANY_ATTRIBUTE_NAME)
        self.assertRaises(ValueError, testable_driver.get_element_attribute, '', ANY_HINT, ANY_ATTRIBUTE_NAME)

        self.assertRaises(ValueError, testable_driver.get_element_attribute, ANY_CSS_PATH, ANY_HINT, None)
        self.assertRaises(ValueError, testable_driver.get_element_attribute, ANY_CSS_PATH, ANY_HINT, '')

    def test_get_attribute_selenium_throws(self):
        testable_driver = DriverTestable()
        element_stub = WebElementStub()

        with patch.object(testable_driver, 'find_element', return_value=element_stub):
            with patch.object(element_stub, 'get_attribute') as element_mock:
                inner_exception = Exception()
                element_mock.side_effect = inner_exception

                try:
                    testable_driver.get_element_attribute(ANY_CSS_PATH, ANY_HINT, ANY_ATTRIBUTE_NAME)
                except NoSuchAttributeError as exception:
                    self.assertEqual(exception.css_path, ANY_CSS_PATH)
                    self.assertEqual(exception.hint, ANY_HINT)
                    self.assertEqual(exception.attribute_name, ANY_ATTRIBUTE_NAME)
                    self.assertEqual(exception.inner_exception, inner_exception)

    def test_get_attribute_selenium_returns_none(self):
        testable_driver = DriverTestable()
        element_stub = WebElementStub()

        with patch.object(testable_driver, 'find_element', return_value=element_stub):
            with patch.object(element_stub, 'get_attribute', return_value=None):

                try:
                    testable_driver.get_element_attribute(ANY_CSS_PATH, ANY_HINT, ANY_ATTRIBUTE_NAME)
                except NoSuchAttributeError as exception:
                    self.assertEqual(exception.css_path, ANY_CSS_PATH)
                    self.assertEqual(exception.hint, ANY_HINT)
                    self.assertEqual(exception.attribute_name, ANY_ATTRIBUTE_NAME)
                    self.assertEqual(exception.inner_exception, None)

    def test_get_attribute_selenium_returns_empty(self):
        testable_driver = DriverTestable()
        element_stub = WebElementStub()

        with patch.object(testable_driver, 'find_element', return_value=element_stub):
            with patch.object(element_stub, 'get_attribute', return_value=''):

                try:
                    testable_driver.get_element_attribute(ANY_CSS_PATH, ANY_HINT, ANY_ATTRIBUTE_NAME)
                except NoSuchAttributeError as exception:
                    self.assertEqual(exception.css_path, ANY_CSS_PATH)
                    self.assertEqual(exception.hint, ANY_HINT)
                    self.assertEqual(exception.attribute_name, ANY_ATTRIBUTE_NAME)
                    self.assertEqual(exception.inner_exception, None)

    def test_get_element_value(self):
        testable_driver = DriverTestable()
        element_stub = WebElementStub()

        with patch.object(testable_driver, 'find_element', return_value=element_stub):
            with patch.object(element_stub, 'text', new_callable=PropertyMock) as element_mock:
                type(element_mock).text = PropertyMock(return_value=ANY_VALUE)

                attribute_value = testable_driver.get_element_value(ANY_CSS_PATH, ANY_HINT)

                self.assertEqual(ANY_VALUE, attribute_value.text)

    def test_get_element_value_exception(self):
        testable_driver = DriverTestable()

        self.assertRaises(ValueError, testable_driver.get_element_value, '', ANY_HINT)
        self.assertRaises(ValueError, testable_driver.get_element_value, None, ANY_HINT)

    def test_click_if_found(self):
        testable_driver = DriverTestable()
        element_stub = WebElementStub()

        with patch.object(testable_driver, '_find_element_with_timeout', return_value=element_stub):
            with patch.object(element_stub, 'click') as element_mock:

                testable_driver.click_if_found(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

                self.assertTrue(element_mock.called)

    def test_click_if_found_not_found(self):
        testable_driver = DriverTestable()
        element_stub = WebElementStub()

        with patch.object(testable_driver, '_find_element_with_timeout', return_value=element_stub) as driver_mock:
            with patch.object(element_stub, 'click') as element_mock:

                driver_mock.side_effect = ElementNotFoundError(ANY_CSS_PATH, ANY_HINT, Exception())

                testable_driver.click_if_found(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

                self.assertFalse(element_mock.called)

    def test_click_if_found_empty_args(self):
        driver_testable = DriverTestable()

        self.assertRaises(ValueError, driver_testable.click_if_found, '', '', ANY_WAIT_TIME)
        self.assertRaises(ValueError, driver_testable.click_if_found, None, '', ANY_WAIT_TIME)

        self.assertRaises(ValueError, driver_testable.click_if_found, ANY_CSS_PATH, '', None)
        self.assertRaises(ValueError, driver_testable.click_if_found, ANY_CSS_PATH, '', -66)

    def test_can_find_element(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, '_find_element_with_timeout') as driver_mock:
            returned_value = driver_testable.can_find_element(ANY_CSS_PATH, ANY_WAIT_TIME)

            driver_mock.assert_called_with(ANY_CSS_PATH, '', ANY_WAIT_TIME)

            self.assertTrue(returned_value)

    def test_can_find_element_error(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, '_find_element_with_timeout') as driver_mock:
            driver_mock.side_effect = ElementNotFoundError(ANY_CSS_PATH, ANY_HINT, None)

            returned_value = driver_testable.can_find_element(ANY_CSS_PATH, ANY_WAIT_TIME)

            driver_mock.assert_called_with(ANY_CSS_PATH, '', ANY_WAIT_TIME)

            self.assertFalse(returned_value)

    def test_can_find_element_empty_args(self):
        driver_testable = DriverTestable()

        self.assertRaises(ValueError, driver_testable.can_find_element, '', ANY_WAIT_TIME)
        self.assertRaises(ValueError, driver_testable.can_find_element, None, ANY_WAIT_TIME)

        self.assertRaises(ValueError, driver_testable.can_find_element, ANY_CSS_PATH, None)
        self.assertRaises(ValueError, driver_testable.can_find_element, ANY_CSS_PATH, -99)

    def test_send_text(self):
        element_stub = WebElementStub()

        driver_testable = DriverTestable()

        with patch.object(element_stub, 'send_keys') as send_keys_mock:
            with patch.object(element_stub, 'clear') as clear_mock:
                with patch.object(driver_testable, 'find_element', return_value=element_stub) as driver_mock:
                    send_keys_mock_calls = [call(Keys.NUMPAD1), call(ANY_TEXT)]

                    driver_testable.send_text(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)

                    driver_mock.assert_called_with(ANY_CSS_PATH, ANY_HINT)
                    send_keys_mock.assert_has_calls(send_keys_mock_calls)

                    self.assertTrue(clear_mock.called)

    def test_send_text_exception(self):
        exception_to_be_thrown = Exception()

        element_stub = WebElementStub()

        driver_testable = DriverTestable()

        with patch.object(element_stub, 'send_keys', side_effect=exception_to_be_thrown):
            with patch.object(driver_testable, 'find_element', return_value=element_stub) as driver_mock:
                try:
                    driver_testable.send_text(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)
                except CannotTypeTextError as exception:
                    self.assertEqual(exception.css_path, ANY_CSS_PATH)
                    self.assertEqual(exception.hint, ANY_HINT)
                    self.assertEqual(exception.text, ANY_TEXT)
                    self.assertEqual(exception.inner_exception, exception_to_be_thrown)

    def test_send_text_empty_text(self):
        driver_testable = DriverTestable()

        self.assertRaises(ValueError, driver_testable.send_text, ANY_CSS_PATH, ANY_HINT, '')
        self.assertRaises(ValueError, driver_testable.send_text, ANY_CSS_PATH, ANY_HINT, None)

        self.assertRaises(ValueError, driver_testable.send_text, '', ANY_HINT, ANY_TEXT)
        self.assertRaises(ValueError, driver_testable.send_text, None, ANY_HINT, ANY_TEXT)

    def test_select_drop_down_item_by_text(self):
        driver_testable = DriverTestable()

        element_stub = WebElementStub()
        element_stub.tag_name = 'select'

        with patch.object(driver_testable, '_get_select', return_value=element_stub) as get_selected_mock, \
                patch.object(element_stub, 'select_by_visible_text') as select_mock, \
                patch.object(driver_testable, 'find_element', return_value=element_stub) as find_element_mock:

            driver_testable.select_drop_down_item_by_text(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)

            find_element_mock.assert_called_with(ANY_CSS_PATH, ANY_HINT)
            get_selected_mock.assert_called_with(element_stub)
            select_mock.assert_called_with(ANY_TEXT)

    def test_select_drop_down_item_by_text_not_select(self):
        driver_testable = DriverTestable()

        element_stub = WebElementStub()
        element_stub.tag_name = 'select'

        with patch.object(driver_testable, '_get_select', return_value=element_stub) as get_selected_mock, \
                patch.object(element_stub, 'select_by_visible_text'), \
                patch.object(driver_testable, 'find_element', return_value=element_stub) as find_element_mock:

            unexpected_tag_ex = UnexpectedTagNameException()

            get_selected_mock.side_effect = unexpected_tag_ex

            try:
                driver_testable.select_drop_down_item_by_text(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)
            except InvalidElementException as exception:
                self.assertEqual(exception.css_path, ANY_CSS_PATH)
                self.assertEqual(exception.hint, ANY_HINT)
                self.assertEqual(exception.inner_exception, unexpected_tag_ex)

                find_element_mock.assert_called_with(ANY_CSS_PATH, ANY_HINT)

    def test_select_drop_down_item_by_text_item_not_found(self):
        driver_testable = DriverTestable()

        element_stub = WebElementStub()
        element_stub.tag_name = 'select'

        with patch.object(driver_testable, '_get_select', return_value=element_stub) as get_selected_mock, \
                patch.object(element_stub, 'select_by_visible_text') as select_mock, \
                patch.object(driver_testable, 'find_element', return_value=element_stub) as find_element_mock:

            no_such_element = NoSuchElementException()

            select_mock.side_effect = no_such_element

            try:
                driver_testable.select_drop_down_item_by_text(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)
            except InvalidOptionTextException as exception:
                self.assertEqual(exception.css_path, ANY_CSS_PATH)
                self.assertEqual(exception.hint, ANY_HINT)
                self.assertEqual(exception.option_text, ANY_TEXT)
                self.assertEqual(exception.inner_exception, no_such_element)

                find_element_mock.assert_called_with(ANY_CSS_PATH, ANY_HINT)
                get_selected_mock.assert_called_with(element_stub)

    def test_select_drop_down_item_empty_text(self):
        driver_testable = DriverTestable()

        self.assertRaises(ValueError, driver_testable.select_drop_down_item_by_text, ANY_CSS_PATH, ANY_HINT, '')
        self.assertRaises(ValueError, driver_testable.select_drop_down_item_by_text, ANY_CSS_PATH, ANY_HINT, None)

        self.assertRaises(ValueError, driver_testable.select_drop_down_item_by_text, None, ANY_HINT, ANY_TEXT)
        self.assertRaises(ValueError, driver_testable.select_drop_down_item_by_text, '', ANY_HINT, ANY_TEXT)


class TestElementNotFoundError(TestCase):
    """Has unit tests for the ElementNotFoundError class"""

    def test_initializer(self):
        any_css_path = 'any css path'
        any_hint = 'any hint'
        any_exception = Exception('foo')

        exception = ElementNotFoundError(any_css_path, any_hint, any_exception)

        self.assertEqual(exception.css_path, any_css_path)
        self.assertEqual(exception.hint, any_hint)
        self.assertEqual(exception.inner_exception, any_exception)


class TestNoSuchAttributeError(TestCase):
    """"Has unit tests for the NoSuchAttributeError class"""

    def test_initializer(self):
        any_css_path = 'any css path'
        any_hint = 'any hint'
        any_attribute_name = 'any attribute name'
        any_exception = Exception('foo')

        exception = NoSuchAttributeError(any_css_path, any_hint, any_attribute_name, any_exception)

        self.assertEqual(exception.css_path, any_css_path)
        self.assertEqual(exception.hint, any_hint)
        self.assertEqual(exception.inner_exception, any_exception)
        self.assertEqual(exception.attribute_name, any_attribute_name)


class TestCannotTypeTextError(TestCase):
    """Has unit tests for the CannotTypeTextError class"""

    def test_initializer(self):
        exception = Exception()

        cannot_type_text = CannotTypeTextError(ANY_CSS_PATH, ANY_HINT, ANY_TEXT, exception)

        self.assertEqual(cannot_type_text.css_path, ANY_CSS_PATH)
        self.assertEqual(cannot_type_text.hint, ANY_HINT)
        self.assertEqual(cannot_type_text.text, ANY_TEXT)
        self.assertEqual(cannot_type_text.inner_exception, exception)


class TestInvalidElementException(TestCase):
    """Has unit tests for the InvalidElementException class"""

    def test_initializer(self):
        exception = Exception()

        invalid_element = InvalidElementException(ANY_CSS_PATH, ANY_HINT, exception)

        self.assertEqual(invalid_element.css_path, ANY_CSS_PATH)
        self.assertEqual(invalid_element.hint, ANY_HINT)
        self.assertEqual(invalid_element.inner_exception, exception)


class TestInvalidOptionTextException(TestCase):
    """Has unit tests for the InvalidOptionTextException class"""

    def test_initializer(self):
        exception = Exception()

        invalid_option = InvalidOptionTextException(ANY_CSS_PATH, ANY_HINT, ANY_TEXT, exception)

        self.assertEqual(invalid_option.css_path, ANY_CSS_PATH)
        self.assertEqual(invalid_option.hint, ANY_HINT)
        self.assertEqual(invalid_option.option_text, ANY_TEXT)
        self.assertEqual(invalid_option.inner_exception, exception)

