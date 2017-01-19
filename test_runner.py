from _selenium_wrapper import Driver


class TestResult:
    """"Represents the result of the execution of a test

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
            raise ValueError('no steps on the test')

        test_result = TestResult()

        with self._get_web_driver() as driver:
            for step in self.test.steps:
                step_result = step.run(driver)
                test_result.add_step_result(step_result)

        return test_result

    def _get_web_driver(self):
        return Driver()
