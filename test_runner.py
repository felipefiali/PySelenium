from _selenium_wrapper import Driver
from step_runner import _run_step


class TestResult:
    """"Represents the result of the execution a test

    Attributes:
        step_results -- Holds the results of every step on the test
    """

    def __init__(self):
        self.step_results = []

    def add_step_result(self, step_result):
        """Adds a new step execution result to the list"""

        self.step_results.append(step_result)


class TestRunner:
    """Runs every test step and collects the execution result"""

    def __init__(self, test):
        self.test = test

    def run_test(self):
        """"Runs the supplied test and returns the result of the execution"""

        if len(self.test.steps) == 0:
            raise ValueError('No steps on the test')

        test_result = TestResult()

        driver = self._get_web_driver()

        for step in self.test.steps:
            test_result.add_step_result(_run_step(step, driver))

        return test_result

    def _get_web_driver(self):
        return Driver()
