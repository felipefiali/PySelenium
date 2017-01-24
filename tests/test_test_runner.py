from unittest import TestCase
from tests.testables import TestRunnerTestable
from tests.testables import DriverTestable
from test_runner import TestResult
from test_runner import TestRunner
from test_metadata import Test
from test_steps import StepResult
from test_steps import Click
from test_steps import Navigate
from test_steps import Step
from mock import patch


class TestTestResult(TestCase):
    """"Has unit tests for the TestResult class"""

    def test_add_step_result(self):
        test_result = TestResult(Test())

        test_result.add_step_result(StepResult(Click()))
        test_result.add_step_result(StepResult(Click()))
        test_result.add_step_result(StepResult(Click()))

        self.assertEqual(3, len(test_result.step_results))


class TestTestRunner(TestCase):
    """"Has unit tests for the TestRunner class"""

    def test_run_test_exception(self):
        test_runner = TestRunner(Test())

        self.assertRaises(ValueError, test_runner.run_test)

    def test_run_test(self):
        with patch.object(Step, 'run') as run_mock:
            test = Test()

            click = Click()
            navigate = Navigate()

            test.add_step(click)
            test.add_step(navigate)

            test_runner_testable = TestRunnerTestable(test)

            driver_testable = DriverTestable()

            test_runner_testable.inject_driver_testable(driver_testable)

            run_mock.run.return_value(StepResult(Click()))

            test_result = test_runner_testable.run_test()

            self.assertEqual(len(test.steps), len(test_result.step_results))
