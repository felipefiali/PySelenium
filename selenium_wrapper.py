from selenium import webdriver


class Driver:
    """A wrapper class for the selenium WebDriver component"""

    def __init__(self):
        super().__init__()

    def __enter__(self):
        """Starts the driver once the object enters context"""
        self.driver = self.get_web_driver()
        return self

    def __exit__(self, type, value, traceback):
        """Closes the driver once the object exits context"""
        if self.driver is not None:
            self.driver.close()
            self.driver = None

    def navigate(self, url):
        """Navigates to the specified URL"""
        self.driver.get(url)

    def get_web_driver(self):
        """Creates an instance of the driver"""
        return webdriver.Chrome()
