from pyselenium._selenium_wrapper import Driver


class TestResult:
    """"Represents the result of the execution of a test

    Attributes:
        step_results -- Holds the results of every step on the test
    """

    def __init__(self, test):
        self.step_results = []
        self.test = test

    def add_step_result(self, step_result):
        """Adds a new step execution result to the list"""

        self.step_results.append(step_result)

    def print_test_result(self):
        """"Prints the test result to the current default stream"""

        for step_result in self.step_results:
            print(type(step_result.step).__name__ + ' - ' + "Success" if step_result.success
                  else str(step_result.exception) + 'Hint')

    def __str__(self):
        string = "[%s] test result" % self.test.test_id
        string += "\n________________________"
        string += "\nSteps:\n"

        for step_result in self.step_results:
            line = "- [%s] - " % type(step_result.step).__name__
            line += "Success" if step_result.success \
                else "%s - %s" % (type(step_result.exception).__name__, str(step_result.exception))

            string += "\n%s" % line

        return string


class TestRunner:
    """Runs every test step and collects the execution result"""

    def __init__(self, test):
        self.test = test

    def run_test(self):
        """"Runs the supplied test and returns the result of the execution"""

        if len(self.test.steps) == 0:
            raise ValueError('no steps on the test')

        test_result = TestResult(self.test)

        with self._get_web_driver() as driver:
            for step in self.test.steps:
                step_result = step.run(driver)
                test_result.add_step_result(step_result)

        return test_result

    def _get_web_driver(self):
        return Driver()
