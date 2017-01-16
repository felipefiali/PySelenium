from PySelenium.TestMetadata import Step
from PySelenium.TestMetadata import ElementFinder


class Click(Step, ElementFinder):
    """A test step that simulates a click on an element"""

    def __init__(self):
        super().__init__()