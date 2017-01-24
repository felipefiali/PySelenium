from test_metadata import ElementFinder
from test_metadata import Step


class Click(ElementFinder, Step):
    """A test step that simulates a click on an element"""

    def __init__(self, css_path, hint):
        super().__init__(css_path, hint)

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.click(self.css_path, self.hint)
        except Exception as exception:
            step_result.exception = exception

        return step_result


class Navigate(Step):
    """A test step that navigates to a given URL"""

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.navigate(self.url)
        except Exception as exception:
            step_result.exception = exception

        return step_result


class AssertAttributeValue(ElementFinder, Step):
    """A test step that compares a given value to a given attribute value of the web element"""

    def __init__(self, css_path, hint, attribute_name, expected_value):
        super().__init__(css_path, hint)

        self.attribute_name = attribute_name
        self.expected_value = expected_value

    def run(self, driver):
        step_result = StepResult(self)
        attribute_value = None

        try:
            attribute_value = driver.get_element_attribute(self.css_path, self.hint, self.attribute_name,
                                                           self.expected_value)
        except Exception as exception:
            step_result.exception = exception
        else:
            if attribute_value != self.expected_value:
                step_result.exception = ElementAttributeValueIncorrectError(self.css_path, self.hint,
                                                                            self.attribute_name,
                                                                            attribute_value, self.expected_value)

        return step_result


class StepResult:
    """Represents the result of the execution of a test step.

    Attributes:
        success -- True if the step execution was successful, false otherwise
        exception -- An exception that might have occurred during step execution. None if no exception occurred
        step -- The step that was executed
     """

    def __init__(self, step):
        self.success = True
        self.step = step
        self._exception = None

    @property
    def exception(self):
        """"Gets an exception if one occurred during execution of the step. Returns None otherwise."""

        return self._exception

    @exception.setter
    def exception(self, value):
        """"Sets the exception that occurred during execution of the step."""

        self._exception = value
        self.success = False


class StepExecutionError(Exception):
    """"Represents failures in test steps execution"""
    pass


class ElementAttributeValueIncorrectError(StepExecutionError):
    """An exception thrown when the value of an element's given attribute is different from the expected value"""

    def __init__(self, css_path, hint, attribute_name, actual_value, expected_value):
        super().__init__()

        self.css_path = css_path
        self.hint = hint
        self.attribute_name = attribute_name
        self.actual_value = actual_value
        self.expected_value = expected_value
