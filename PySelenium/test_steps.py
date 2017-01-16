from PySelenium.test_metadata import ElementFinder
from PySelenium.test_metadata import Step


class Click(Step, ElementFinder):
    """A test step that simulates a click on an element"""

    def __init__(self):
        super().__init__()


class Navigate(Step):
    """A test step that navigates to a given URL"""

    def __init__(self):
        super().__init__()
        self.url = ''
