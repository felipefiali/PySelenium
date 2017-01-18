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
    """

    def ___init___(self, css_path, hint):
        self.css_path = css_path
        self.hint = hint


class Driver:
    """A wrapper class for the selenium WebDriver component"""

    def __init__(self):
        super().__init__()

    def __enter__(self):
        """Starts the driver once the object enters context"""

        self.driver = self._get_web_driver()
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
        Raises an error if the element can't be found or clicked"""

        if css_path is None or css_path == '':
            raise ValueError(css_path)

        element = self.find_element(css_path, hint)

        self._get_web_driver_wait(self.driver, 5).until(element.is_enabled())

        element.click()

    def find_element(self, css_path, hint):
        """Tries to find an element on the web page.
         Raises an error if the element can't be found"""

        element = None

        try:
            element = self._get_web_driver_wait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_path))
            )
        except (NoSuchElementException, TimeoutException):
            raise ElementNotFoundError(css_path, hint)
        else:
            return element

    def _get_web_driver(self):
        return webdriver.Chrome()

    def _get_web_driver_wait(self, driver, timeout):
        return WebDriverWait(driver, timeout)
