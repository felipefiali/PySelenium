from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


class ElementNotFoundError(Exception):
    """Exception raised when the element referenced in a step is not found

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
    """Exception raised when the web element does not have a specified attribute

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

        element = None

        try:
            element = self._get_web_driver_wait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, css_path))
            )
        except Exception as exception:
            raise ElementNotFoundError(css_path, hint, exception)

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

        element = None

        try:
            element = self._get_web_driver_wait(self.driver, 10).until(
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
