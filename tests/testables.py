from _selenium_wrapper import Driver
from selenium.webdriver.support.ui import WebDriverWait


class DriverStub:
    """A stub of Selenium's Driver class to enable unit testing of the wrapper class"""

    def get(self, url):
        print('- get method called on DriverStub with url: ' + url)

    def close(self):
        print('- close method called on DriverStub')


class WebElementStub:
    """"A stub that allows unit testing of interactions with web elements"""

    def click(self):
        print('web element clicked')
        pass

    def is_enabled(self):
        return True


class DriverTestable(Driver):
    """A testable version of the Driver class which doesn't actually interact with Selenium"""

    def __init__(self):
        super().__init__()
        self.driver = DriverStub()
        self.web_driver_wait_testable = WebDriverWaitTestable()

    def _get_web_driver(self):
        return self.driver

    def _get_web_driver_wait(self, driver, timeout):
        return self.web_driver_wait_testable

    def inject_web_driver_wait_testable(self, web_driver_wait_testable):
        self.web_driver_wait_testable = web_driver_wait_testable


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
