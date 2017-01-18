from test_steps import Click
from test_steps import Navigate


class StepResult:
    """Represents the result of the execution of a test step.

    Attributes:
        success -- True if the step execution was successful, false otherwise
        exception -- An exception that might have occurred during step execution. None if no exception occurred
        step -- The step that was executed
     """

    def __init__(self, step):
        self.success = True
        self.exception = None
        self.step = step

    @property
    def exception(self):
        """"Gets an exception if one occurred during execution of the step. Returns None otherwise."""

        return self.exception

    @exception.setter
    def exception(self, value):
        """"Sets the exception that occurred during execution of the step."""

        self.exception = value
        self.success = False


def _run_click(click, driver):
    """"Runs Click test steps"""

    step_result = StepResult(click)

    try:
        driver.click(click.css_path, click.hint)
    except Exception as exception:
        step_result.exception = exception

    return step_result


def _run_navigate(navigate, driver):
    """"Runs Navigate test steps"""

    step_result = StepResult(navigate)

    try:
        driver.navigate(navigate.url)
    except Exception as exception:
        step_result.exception = exception

    return step_result


def _run_step(step, driver):
    """"Runs a test step accordingly"""

    function = None

    if step is Click:
        function = _run_click
    elif step is Navigate:
        function = _run_navigate

    return function(step, driver)
