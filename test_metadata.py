class Test:
    """"The base class for the tests"""

    def __init__(self):
        self.steps = []

    def add_step(self, step):
        """Adds a test step to the test"""
        self.steps.append(step)


class Step:
    """The base class for test steps"""

    def __init__(self):
        super().__init__()


class ElementFinder:
    """A base class that specifies that a step is able to find HTML elements"""

    def __init__(self):
        super().__init__()
        self.cssPath = ''
        self.hint = ''
