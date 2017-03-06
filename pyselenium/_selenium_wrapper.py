from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedTagNameException
from selenium.common.exceptions import NoSuchFrameException


class ElementNotFoundError(Exception):
    """Exception raised when the element referenced in a step is not found.

    Attributes:
        css_path -- The supplied CSS path of the element
        hint -- The element hint
        inner_exception -- The exception that may have been thrown by the web driver, None otherwise
    """

    def __init__(self, css_path, hint, exception):
        self.css_path = css_path
        self.hint = hint
        self.inner_exception = exception


class NoSuchAttributeError(Exception):
    """Exception raised when the web element does not have a specified attribute.

    Attributes:
        css_path -- The CSS path of the element
        hint -- The element hint
        attribute_name -- The name of the missing attribute
        inner_exception -- The exception that may have been thrown by the web driver, None otherwise
    """

    def __init__(self, css_path, hint, attribute_name, exception):
        self.css_path = css_path
        self.hint = hint
        self.attribute_name = attribute_name
        self.inner_exception = exception


class CannotTypeTextError(Exception):
    """Exception raised when the web element is found but the typing of the text fails for some reason.

    Attributes:
        css_path -- The CSS path of the element
        hint -- The element hint
        text -- The text to be typed on the element
        inner_exception -- The exception that may have been thrown by the web driver, None otherwise
    """

    def __init__(self, css_path, hint, text, exception):
        self.css_path = css_path
        self.hint = hint
        self.text = text
        self.inner_exception = exception


class InvalidElementException(Exception):
    """Exception raised when an invalid operation is performed on a web element.

    Attributes:
        css_path -- The CSS path of the element
        hint -- The element hint
        inner_exception -- The exception that may have been thrown by the web driver, None otherwise
    """

    def __init__(self, css_path, hint, exception):
        self.css_path = css_path
        self.hint = hint
        self.inner_exception = exception


class InvalidOptionTextException(Exception):
    """Exception raised when there is no option with the specified text in the Select web element.

    Attributes:
        css_path -- The CSS path of the element
        hint -- The element hint
        option_text -- The invalid specified option text
        inner_exception -- The exception that may have been thrown by the web driver, None otherwise
    """

    def __init__(self, css_path, hint, option_text, exception):
        self.css_path = css_path
        self.hint = hint
        self.option_text = option_text
        self.inner_exception = exception


class UnknownErrorException(Exception):
    """Exception raised when an unknown error occurs in Selenium Web Driver.

    Attributes:
        inner_exception -- The exception that has been thrown by the web driver
    """

    def __init__(self, exception):
        self.inner_exception = exception


class Driver:
    """A wrapper class for the selenium WebDriver component"""

    def __init__(self):
        super().__init__()

    def __enter__(self):
        """Starts the driver once the object enters context"""

        self.driver = self._get_web_driver()
        self.driver.maximize_window()

        return self

    def __exit__(self, type, value, traceback):
        """Closes the driver once the object exits context"""

        if self.driver is not None:
            self.driver.close()
            self.driver = None

    def navigate(self, url):
        """Navigates to the specified URL"""

        if url is None:
            raise TypeError('url')

        if url == '':
            raise ValueError('url')

        self.driver.get(url)

    def click(self, css_path, hint):
        """Tries to find an element on the web page and click it.
        Raises an error if the element can't be found or clicked."""

        if css_path is None or css_path == '':
            raise ValueError('css_path')

        try:
            element = self._get_web_driver_wait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, css_path))
            )
        except Exception as exception:
            raise ElementNotFoundError(css_path, hint, exception)

        element.click()

    def click_if_found(self, css_path, hint, wait_time):
        """Tries to click an element on the web page for the time specified as the wait time.
        Does nothing if the element is not found."""

        if css_path is None or css_path == '':
            raise ValueError('css-path')

        if wait_time is None or wait_time < 0:
            raise ValueError('wait_time')

        try:
            element = self._find_element_with_timeout(css_path, hint, wait_time)
        except ElementNotFoundError:
            pass
        else:
            element.click()

    def get_element_attribute(self, css_path, hint, attribute_name):
        """"Tries to get an attribute value from an element on the web page.
        Raises errors if the element can't be found or if it doesn't have the specified attribute."""

        if css_path is None or css_path == '':
            raise ValueError('css_path')

        if attribute_name is None or attribute_name == '':
            raise ValueError('attribute_name')

        element = self.find_element(css_path, hint)

        try:
            attribute_value = element.get_attribute(attribute_name)
        except Exception as exception:
            raise NoSuchAttributeError(css_path, hint, attribute_name, exception)

        if attribute_value is None or attribute_value == '':
            raise NoSuchAttributeError(css_path, hint, attribute_name, None)

        return attribute_value

    def get_element_value(self, css_path, hint):
        """Tries to get the value of an element on the web page.
        Raises errors if the element can't be found."""

        if css_path is None or css_path == '':
            raise ValueError('css_path')

        element = self.find_element(css_path, hint)

        return element.text

    def find_element(self, css_path, hint):
        """Tries to find an element on the web page.
         Raises an error if the element can't be found."""

        if css_path is None or css_path == '':
            raise ValueError('css_path')

        return self._find_element_with_timeout(css_path, hint, 10)

    def can_find_element(self, css_path, wait_time):
        """Tries to find an element at the given CSS path. Returns true if one is found, false otherwise."""

        if css_path is None or css_path == '':
            raise ValueError('css_path')

        if wait_time is None or wait_time < 0:
            raise ValueError('wait_time')

        try:
            self._find_element_with_timeout(css_path, '', wait_time)
        except ElementNotFoundError:
            return False
        else:
            return True

    def send_text(self, css_path, hint, text):
        """Finds an element and sends the specified text to it as if the user typed it.
        Raises errors if the element can not be found."""

        if text is None or text == '':
            raise ValueError('text')

        element = self.find_element(css_path, hint)

        try:
            # We do the following to trigger any JS events on the element before sending the actual text:
            element.send_keys(Keys.NUMPAD1)
            element.clear()

            element.send_keys(text)
        except Exception as exception:
            raise CannotTypeTextError(css_path, hint, text, exception)

    def send_enter_key(self):
        """Sends the enter key to the page as if the user had pressed the return button on the keyboard."""

        try:
            self._get_action_chains().send_keys(Keys.RETURN).perform()
        except Exception as exception:
            raise UnknownErrorException(exception)

    def select_drop_down_item_by_text(self, css_path, hint, item_text):
        """Finds a Select element and selects an item by its text.
        Raises errors if the element can not be found or if it is not a Select web element."""

        if item_text is None or item_text == '':
            raise ValueError('item_text')

        element = self.find_element(css_path, hint)

        try:
            self._get_select(element).select_by_visible_text(item_text)
        except UnexpectedTagNameException as unexpected_tag_ex:
            raise InvalidElementException(css_path, hint, unexpected_tag_ex)
        except NoSuchElementException as invalid_item_text:
            raise InvalidOptionTextException(css_path, hint, item_text, invalid_item_text)

    def set_checkbox(self, css_path, hint, checked):
        """Finds a checkbox element and checks or unchecks it by clicking on it.
        Raises errors if the element can not be found."""

        if css_path is None or css_path == '':
            raise ValueError('css_path')

        if checked is None:
            raise ValueError('checked')

        element = self.find_element(css_path, hint)

        if element.is_selected() != checked:
            element.click()

    def switch_to_frame(self, css_path, hint):
        """Switches the context of the web driver to the frame at the specified CSS path.
        Raises errors if the frame can not be found."""

        if css_path is None or css_path == '':
            raise ValueError('css_path')

        frame = self.find_element(css_path, hint)

        try:
            self.driver.switch_to.frame(frame)
        except NoSuchFrameException as exception:
            raise InvalidElementException(css_path, hint, exception)

    def switch_to_default_content(self):
        """Switches the context of the web driver to the default content of the page."""

        self.driver.switch_to.default_content()

    def _find_element_with_timeout(self, css_path, hint, timeout):
        try:
            element = self._get_web_driver_wait(self.driver, timeout).until(
                self._get_presence_of_element_located(css_path)
            )
        except (NoSuchElementException, TimeoutException) as exception:
            raise ElementNotFoundError(css_path, hint, exception)
        else:
            return element

    def _get_web_driver(self):
        return webdriver.Chrome()

    def _get_web_driver_wait(self, driver, timeout):
        return WebDriverWait(driver, timeout)

    def _get_presence_of_element_located(self, css_path):
        return expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_path))

    def _get_select(self, web_element):
        return Select(web_element)

    def _get_action_chains(self):
        return ActionChains(self.driver)

