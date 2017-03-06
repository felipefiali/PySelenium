from pyselenium.test_metadata import ElementFinder
from pyselenium.test_metadata import Step


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


class AssertElementValue(ElementFinder, Step):
    """A test step that asserts the value (text) inside an element"""

    def __init__(self, css_path, hint, expected_value):
        super().__init__(css_path, hint)

        self.expected_value = expected_value

    def run(self, driver):
        step_result = StepResult(self)

        element_value = None

        try:
            element_value = driver.get_element_value(self.css_path, self.hint)
        except Exception as exception:
            step_result.exception = exception
        else:
            if element_value != self.expected_value:
                step_result.exception = ElementValueIncorrectError(self.css_path, self.hint, element_value,
                                                                   self.expected_value)

        return step_result


class AssertElementAttributeValue(ElementFinder, Step):
    """A test step that compares a given value to a given attribute value of the web element"""

    def __init__(self, css_path, hint, attribute_name, expected_value):
        super().__init__(css_path, hint)

        self.attribute_name = attribute_name
        self.expected_value = expected_value

    def run(self, driver):
        step_result = StepResult(self)
        attribute_value = None

        try:
            attribute_value = driver.get_element_attribute(self.css_path, self.hint, self.attribute_name)
        except Exception as exception:
            step_result.exception = exception
        else:
            if attribute_value != self.expected_value:
                step_result.exception = ElementAttributeValueIncorrectError(self.css_path, self.hint,
                                                                            self.attribute_name,
                                                                            attribute_value, self.expected_value)

        return step_result


class ClickIfFound(ElementFinder, Step):
    """A test step that clicks an element if it is found but doesn't fail if it's not found"""

    def __init__(self, css_path, hint, wait_time):
        super().__init__(css_path, hint)

        self.wait_time = wait_time

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.click_if_found(self.css_path, self.hint, self.wait_time)
        except Exception as exception:
            step_result.exception = exception

        return step_result


class AssertElementNotPresent(ElementFinder, Step):
    """Asserts that an element at a given CSS path is not present on the web page
     after trying to find it for a given time"""

    def __init__(self, css_path, hint, wait_time):
        super().__init__(css_path, hint)

        self.wait_time = wait_time

    def run(self, driver):
        step_result = StepResult(self)

        try:
            element_found = driver.can_find_element(self.css_path, self.wait_time)
        except Exception as exception:
            step_result.exception = exception
        else:
            if element_found:
                step_result.exception = ElementShouldNotBePresentError(self.css_path, self.hint, self.wait_time)

        return step_result


class TypeText(ElementFinder, Step):
    """Selects an element and simulates the user typing the specified text in the element"""

    def __init__(self, css_path, hint, text):
        super().__init__(css_path, hint)

        self.text = text

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.send_text(self.css_path, self.hint, self.text)
        except Exception as exception:
            step_result.exception = exception

        return step_result


class SendEnter(Step):
    """Sends the enter key to simulate the user hitting the return button on the keyboard"""

    def __init__(self):
        super().__init__()

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.send_enter_key()
        except Exception as exception:
            step_result.exception = exception

        return step_result


class SelectDropDownItemByText(ElementFinder, Step):
    """Selects an item inside a dropdown control by its text"""

    def __init__(self, css_path, hint, item_text):
        super().__init__(css_path, hint)

        self.item_text = item_text

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.select_drop_down_item_by_text(self.css_path, self.hint, self.item_text)
        except Exception as exception:
            step_result.exception = exception

        return step_result


class SetCheckbox(ElementFinder, Step):
    """Checks or unchecks a checkbox web element"""

    def __init__(self, css_path, hint, checked):
        super().__init__(css_path, hint)

        self.checked = checked

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.set_checkbox(self.css_path, self.hint, self.checked)
        except Exception as exception:
            step_result.exception = exception

        return step_result


class SwitchFrame(ElementFinder, Step):
    """"Switches the context of the web driver to the iFrame found at the specified CSS path"""

    def __init__(self, css_path, hint):
        super().__init__(css_path, hint)

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.switch_to_frame(self.css_path, self.hint)
        except Exception as exception:
            step_result.exception = exception

        return step_result


class SwitchToDefaultContent(Step):
    """Switches the context of the web driver back to the default content of the web page"""

    def run(self, driver):
        step_result = StepResult(self)

        try:
            driver.switch_to_default_content()
        except Exception as exception:
            step_result.exception = exception

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


class ElementValueIncorrectError(StepExecutionError):
    """"An exception thrown when the value of an element is different from the expected value"""

    def __init__(self, css_path, hint, actual_value, expected_value):
        super().__init__()

        self.css_path = css_path
        self.hint = hint
        self.actual_value = actual_value
        self.expected_value = expected_value


class ElementShouldNotBePresentError(StepExecutionError):
    """An exception thrown when an element that should not be present on the web page is found

    Attributes:
        - wait_time: A value, in seconds, that Selenium will keep looking for the element before considering that it is
        not present
    """

    def __init__(self, css_path, hint, wait_time):
        super().__init__()

        self.css_path = css_path
        self.hint = hint
        self.wait_time = wait_time
