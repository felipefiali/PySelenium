from selenium import webdriver


class Driver:
    """A wrapper class for the selenium WebDriver component"""

    def __init(self):
        super().__init__()

    def __enter__(self):
        self.driver = self.get_web_driver()
        return self

    def __exit__(self, type, value, traceback):
        if self.driver is not None:
            self.driver.close()
            self.driver = None

    def navigate(self, url):
        self.driver.get(url)

    def get_web_driver(self):
        return webdriver.Chrome()
