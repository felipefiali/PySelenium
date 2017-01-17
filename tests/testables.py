from selenium_wrapper import Driver


class DriverStub:
    """A stub of Selenium's Driver class to enable unit testing of the wrapper class"""

    def get(self, url):
        print('- get method called on DriverStub with url: ' + url)

    def close(self):
        print('- close method called on DriverStub')


class DriverTestable(Driver):
    """A testable version of the Driver class which doesn't actually interact with Selenium"""

    def __init__(self):
        super().__init__()
        self.driver = DriverStub()

    def get_web_driver(self):
        """Overrides the original method to return a stub instead of the real driver"""
        return self.driver
