from _selenium_wrapper import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from test_runner import TestRunner


class DriverStub:
    """A stub of Selenium's Driver class to enable unit testing of the wrapper class"""

    def get(self, url):
        pass

    def close(self):
        pass

    def maximize_window(self):
        pass


class WebElementStub:
    """"A stub that allows unit testing of interactions with web elements"""

    def __init__(self):
        self.text = ''

    def click(self):
        pass

    def clear(self):
        pass

    def send_keys(self):
        pass

    def is_enabled(self):
        return True

    def get_attribute(self, attribute_name):
        return attribute_name

    def select_by_visible_text(self, item_text):
        pass


class DriverTestable(Driver):
    """A testable version of the Driver class which doesn't actually interact with Selenium"""

    def __init__(self):
        super().__init__()
        self.driver = DriverStub()
        self.web_driver_wait_testable = WebDriverWaitTestable()
        self.presence_of_element_located = expected_conditions.presence_of_element_located(None)

    def _get_web_driver(self):
        return self.driver

    def _get_web_driver_wait(self, driver, timeout):
        return self.web_driver_wait_testable

    def inject_web_driver_wait_testable(self, web_driver_wait_testable):
        self.web_driver_wait_testable = web_driver_wait_testable

    def _get_presence_of_element_located(self, css_path):
        return self.presence_of_element_located

    def inject_presence_of_element_located(self, presence_condition):
        self.presence_of_element_located = presence_condition

    def _get_select(self, web_element):
        return web_element


class WebDriverWaitTestable(WebDriverWait):
    """"A testable version of the WebDriverWait class which doesn't actually interact with Selenium"""

    def __init__(self):
        self.web_element_stub = WebElementStub()
        self.should_raise_error_on_until = False
        self.exception_to_be_raised = None

    def until(self, method, message=''):
        if self.should_raise_error_on_until:
            raise self.exception_to_be_raised

        return self.web_element_stub

    def inject_web_element_stub(self, web_element_stub):
        self.web_element_stub = web_element_stub

    def stub_exception_to_be_raised_on_until(self, exception):
        self.should_raise_error_on_until = True
        self.exception_to_be_raised = exception


class TestRunnerTestable(TestRunner):
    """"A testable version of the TestRunner class"""

    def __init__(self, test):
        super().__init__(test)
        self.driver_testable = DriverTestable()

    def _get_web_driver(self):
        return self.driver_testable

    def inject_driver_testable(self, driver_testable):
        self.driver_testable = driver_testable
