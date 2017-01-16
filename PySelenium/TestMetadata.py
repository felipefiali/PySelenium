class Test:
    """"The base class for the tests"""

    def __init__(self):
        self.currentStepCounter = 1
        self.steps = []

    def add_step(self, step):
        step.order = self.currentStepCounter

        self.steps.append(step)

        self.currentStepCounter += 1


class Step:
    """The base class for test steps"""

    def __init__(self):
        super().__init__()
        self.order = 0


class ElementFinder:
    """A base class that specifies that a step is able to find HTML elements"""

    def __init__(self):
        super().__init__()
        self.cssPath = ''
        self.hint = ''
