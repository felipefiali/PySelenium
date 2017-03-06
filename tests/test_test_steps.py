from unittest import TestCase

from mock import patch

from pyselenium.test_steps import *
from tests.test_data import *
from tests.testables import DriverTestable


class TestStepResult(TestCase):
    """"Has unit tests for the StepResult class"""

    def test_initializer(self):
        click = any_click()

        step_result = StepResult(click)

        self.assertIsNone(step_result.exception)
        self.assertTrue(step_result.success)
        self.assertEqual(click, step_result.step)

    def test_add_exception(self):
        exception = TypeError()

        step_result = StepResult(any_click())
        step_result.exception = exception

        self.assertEqual(step_result.exception, exception)
        self.assertFalse(step_result.success)


class TestElementAttributeValueIncorrectError(TestCase):
    """Has unit tests for the ElementAttributeValueIncorrectError class"""

    def test_initializer(self):
        exception = ElementAttributeValueIncorrectError(ANY_CSS_PATH, ANY_HINT, ANY_ATTRIBUTE_NAME, ANY_OTHER_VALUE,
                                                        ANY_VALUE)

        self.assertEqual(exception.css_path, ANY_CSS_PATH)
        self.assertEqual(exception.hint, ANY_HINT)
        self.assertEqual(exception.attribute_name, ANY_ATTRIBUTE_NAME)
        self.assertEqual(exception.actual_value, ANY_OTHER_VALUE)
        self.assertEqual(exception.expected_value, ANY_VALUE)


class TestClick(TestCase):
    """"Has unit tests for the Click class"""

    def test_initializer(self):
        click = Click(ANY_CSS_PATH, ANY_HINT)

        self.assertEqual(ANY_CSS_PATH, click.css_path)
        self.assertEqual(ANY_HINT, click.hint)

    def test_run_click_exception(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'click') as click_mock:
            exception = Exception()
            click_mock.side_effect = exception
            click = any_click()

            step_result = click.run(driver_testable)

            click_mock.assert_called_with(click.css_path, click.hint)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, click)
            self.assertEqual(step_result.exception, exception)

    def test_run_click(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'click') as click_mock:
            click = any_click()

            step_result = click.run(driver_testable)

            click_mock.assert_called_with(click.css_path, click.hint)
            self.assertTrue(step_result.success)
            self.assertEqual(step_result.step, click)
            self.assertIsNone(step_result.exception)


class TestClickIfFound(TestCase):
    """"Has Unit tests for the ClickIfFound class"""

    def test_initializer(self):
        click_if_found = ClickIfFound(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

        self.assertEqual(click_if_found.css_path, ANY_CSS_PATH)
        self.assertEqual(click_if_found.hint, ANY_HINT)

    def test_click_if_found(self):
        click_if_found = ClickIfFound(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'click_if_found') as mock_driver:
            step_result = click_if_found.run(driver_testable)

            mock_driver.assert_called_with(click_if_found.css_path, click_if_found.hint, click_if_found.wait_time)

            self.assertTrue(step_result.success)
            self.assertEqual(step_result.step, click_if_found)
            self.assertIsNone(step_result.exception)

    def test_click_if_found_exception(self):
        click_if_found = ClickIfFound(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'click_if_found') as mock_driver:
            exception = Exception()
            mock_driver.side_effect = exception
            step_result = click_if_found.run(driver_testable)

            mock_driver.assert_called_with(click_if_found.css_path, click_if_found.hint, click_if_found.wait_time)

            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, click_if_found)
            self.assertEqual(step_result.exception, exception)


class TestNavigate(TestCase):
    """"Has unit tests for the Navigate class"""
    def test_initializer(self):
        navigate = Navigate(ANY_URL)

        self.assertEqual(ANY_URL, navigate.url)

    def test_run_navigate(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'navigate') as navigate_mock:
            navigate = any_navigate()

            step_result = navigate.run(driver_testable)

            navigate_mock.assert_called_with(navigate.url)
            self.assertTrue(step_result.success)
            self.assertEqual(step_result.step, navigate)

    def test_run_navigate_exception(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'navigate') as navigate_mock:
            exception = Exception()
            navigate_mock.side_effect = exception
            navigate = any_navigate()

            step_result = navigate.run(driver_testable)

            navigate_mock.assert_called_with(navigate.url)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, navigate)
            self.assertEqual(step_result.exception, exception)


class TestAssertElementAttributeValue(TestCase):
    """"Has unit tests for the AssertElementAttributeValue class"""

    def test_initializer(self):
        assert_attribute = AssertElementAttributeValue(ANY_CSS_PATH, ANY_HINT, ANY_ATTRIBUTE_NAME, ANY_VALUE)

        self.assertEqual(assert_attribute.css_path, ANY_CSS_PATH)
        self.assertEqual(assert_attribute.hint, ANY_HINT)
        self.assertEqual(assert_attribute.attribute_name, ANY_ATTRIBUTE_NAME)
        self.assertEqual(assert_attribute.expected_value, ANY_VALUE)

    def test_run_assert_attribute(self):
        driver_testable = DriverTestable()

        assert_attribute = any_assert_attribute()

        with patch.object(driver_testable, 'get_element_attribute', return_value=assert_attribute.expected_value) \
                as driver_mock:
            step_result = assert_attribute.run(driver_testable)

            driver_mock.assert_called_with(assert_attribute.css_path, assert_attribute.hint,
                                           assert_attribute.attribute_name)

            self.assertTrue(step_result.success)
            self.assertEqual(step_result.step, assert_attribute)

    def test_run_assert_attribute_different_values(self):
        driver_testable = DriverTestable()

        assert_attribute = any_assert_attribute()

        with patch.object(driver_testable, 'get_element_attribute', return_value=ANY_OTHER_VALUE) \
                as assert_value_mock:
            assert_attribute = any_assert_attribute()

            step_result = assert_attribute.run(driver_testable)

            assert_value_mock.assert_called_with(assert_attribute.css_path, assert_attribute.hint,
                                                 assert_attribute.attribute_name)

            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, assert_attribute)

            assertion_exception = step_result.exception

            self.assertEqual(assertion_exception.css_path, assert_attribute.css_path)
            self.assertEqual(assertion_exception.hint, assert_attribute.hint)
            self.assertEqual(assertion_exception.attribute_name, assert_attribute.attribute_name)
            self.assertEqual(assertion_exception.expected_value, assert_attribute.expected_value)
            self.assertEqual(assertion_exception.actual_value, ANY_OTHER_VALUE)

    def test_run_assert_attribute_exception(self):
        driver_testable = DriverTestable()

        assert_attribute = any_assert_attribute()

        with patch.object(driver_testable, 'get_element_attribute', return_value=assert_attribute.expected_value) \
                as assert_value_mock:
            exception = Exception()
            assert_value_mock.side_effect = exception

            step_result = assert_attribute.run(driver_testable)

            assert_value_mock.assert_called_with(assert_attribute.css_path, assert_attribute.hint,
                                                 assert_attribute.attribute_name)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, assert_attribute)
            self.assertEqual(step_result.exception, exception)


class TestAssertElementValue(TestCase):
    """Has unit tests for the AssertElementValue class"""

    def test_initializer(self):
        assert_element = AssertElementValue(ANY_CSS_PATH, ANY_HINT, ANY_VALUE)

        self.assertEqual(assert_element.css_path, ANY_CSS_PATH)
        self.assertEqual(assert_element.hint, ANY_HINT)
        self.assertEqual(assert_element.expected_value, ANY_VALUE)

    def test_run_assert_element_value(self):
        driver_testable = DriverTestable()

        assert_element = AssertElementValue(ANY_CSS_PATH, ANY_HINT, ANY_VALUE)

        with patch.object(driver_testable, 'get_element_value', return_value=ANY_VALUE) as driver_mock:
            step_result = assert_element.run(driver_testable)

            driver_mock.assert_called_with(assert_element.css_path, assert_element.hint)

            self.assertTrue(step_result.success)
            self.assertEqual(step_result.step, assert_element)
            self.assertIsNone(step_result.exception)

    def test_run_assert_element_different_values(self):
        driver_testable = DriverTestable()

        assert_element = AssertElementValue(ANY_CSS_PATH, ANY_HINT, ANY_VALUE)

        with patch.object(driver_testable, 'get_element_value', return_value=ANY_OTHER_VALUE) as driver_mock:
            step_result = assert_element.run(driver_testable)

            driver_mock.assert_called_with(assert_element.css_path, assert_element.hint)

            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, assert_element)
            self.assertEqual(step_result.exception.css_path, ANY_CSS_PATH)
            self.assertEqual(step_result.exception.hint, ANY_HINT)
            self.assertEqual(step_result.exception.expected_value, ANY_VALUE)
            self.assertEqual(step_result.exception.actual_value, ANY_OTHER_VALUE)

    def test_assert_value_selenium_throws(self):
        driver_testable = DriverTestable()

        assert_element = AssertElementValue(ANY_CSS_PATH, ANY_HINT, ANY_VALUE)

        with patch.object(driver_testable, 'get_element_value') as driver_mock:
            exception = Exception()

            driver_mock.side_effect = exception

            step_result = assert_element.run(driver_testable)

            driver_mock.assert_called_with(assert_element.css_path, assert_element.hint)

            self.assertFalse(step_result.success)
            self.assertEqual(step_result.exception, exception)


class TestAssertElementNotPresent(TestCase):
    """Has unit tests for the AssertElementNotPresent class"""

    def test_initializer(self):
        element_not_present = AssertElementNotPresent(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

        self.assertEqual(element_not_present.css_path, ANY_CSS_PATH)
        self.assertEqual(element_not_present.hint, ANY_HINT)
        self.assertEqual(element_not_present.wait_time, ANY_WAIT_TIME)

    def test_assert_element_not_present(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'can_find_element', return_value=False) as driver_mock:
            assert_element_not_present = AssertElementNotPresent(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

            step_result = assert_element_not_present.run(driver_testable)

            driver_mock.assert_called_with(ANY_CSS_PATH, ANY_WAIT_TIME)

            self.assertIsNone(step_result.exception)
            self.assertEqual(step_result.step, assert_element_not_present)
            self.assertTrue(step_result.success)

    def test_assert_element_not_present_fails(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'can_find_element', return_value=True) as driver_mock:
            assert_element_not_present = AssertElementNotPresent(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

            step_result = assert_element_not_present.run(driver_testable)

            driver_mock.assert_called_with(ANY_CSS_PATH, ANY_WAIT_TIME)

            self.assertEqual(step_result.exception.css_path, ANY_CSS_PATH)
            self.assertEqual(step_result.exception.hint, ANY_HINT)
            self.assertEqual(step_result.exception.wait_time, ANY_WAIT_TIME)
            self.assertEqual(step_result.step, assert_element_not_present)
            self.assertFalse(step_result.success)

    def test_assert_element_not_present_selenium_throws(self):
        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'can_find_element') as driver_mock:
            exception = Exception()

            driver_mock.side_effect = exception

            assert_element_not_present = AssertElementNotPresent(ANY_CSS_PATH, ANY_HINT, ANY_WAIT_TIME)

            step_result = assert_element_not_present.run(driver_testable)

            driver_mock.assert_called_with(ANY_CSS_PATH, ANY_WAIT_TIME)

            self.assertEqual(step_result.exception, exception)
            self.assertEqual(step_result.step, assert_element_not_present)
            self.assertFalse(step_result.success)


class TestTypeText(TestCase):
    """Has unit tests for the TypeText class"""

    def test_initializer(self):
        type_text = TypeText(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)

        self.assertEqual(type_text.css_path, ANY_CSS_PATH)
        self.assertEqual(type_text.hint, ANY_HINT)
        self.assertEqual(type_text.text, ANY_TEXT)

    def test_run_type_text(self):
        driver_testable = DriverTestable()

        type_text = TypeText(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)

        with patch.object(driver_testable, 'send_text') as driver_mock:
            step_result = type_text.run(driver_testable)

            driver_mock.assert_called_with(type_text.css_path, type_text.hint, type_text.text)

            self.assertEqual(step_result.step, type_text)
            self.assertIsNone(step_result.exception)
            self.assertTrue(step_result.success)

    def test_run_type_text_exception(self):
        driver_testable = DriverTestable()

        type_text = TypeText(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)

        with patch.object(driver_testable, 'send_text') as driver_mock:
            exception = Exception()

            driver_mock.side_effect = exception

            step_result = type_text.run(driver_testable)

            driver_mock.assert_called_with(type_text.css_path, type_text.hint, type_text.text)

            self.assertEqual(step_result.step, type_text)
            self.assertEqual(step_result.exception, exception)
            self.assertFalse(step_result.success)


class TestSendEnter(TestCase):
    """Has unit tests for the SendEnter class"""

    def test_run_send_enter(self):
        driver_testable = DriverTestable()

        send_enter = SendEnter()

        with patch.object(driver_testable, 'send_enter_key') as driver_mock:
            step_result = send_enter.run(driver_testable)

            self.assertTrue(driver_mock.called)

            self.assertEqual(step_result.step, send_enter)
            self.assertIsNone(step_result.exception)
            self.assertTrue(step_result.success)

    def test_run_send_enter_exception(self):
        exception = Exception()

        driver_testable = DriverTestable()

        send_enter = SendEnter()

        with patch.object(driver_testable, 'send_enter_key') as driver_mock:
            driver_mock.side_effect = exception

            step_result = send_enter.run(driver_testable)

            self.assertTrue(driver_mock.called)

            self.assertEqual(step_result.step, send_enter)
            self.assertEqual(step_result.exception, exception)
            self.assertFalse(step_result.success)


class TestSelectDropDownItemByText(TestCase):
    """Has unit tests for the SelectDropDownItemByText class"""

    def test_initializer(self):
        select_item = SelectDropDownItemByText(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)

        self.assertEqual(select_item.css_path, ANY_CSS_PATH)
        self.assertEqual(select_item.hint, ANY_HINT)
        self.assertEqual(select_item.item_text, ANY_TEXT)

    def test_run_select_dropdown_item(self):
        driver_testable = DriverTestable()

        select_item = SelectDropDownItemByText(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)

        with patch.object(driver_testable, 'select_drop_down_item_by_text') as driver_mock:
            step_result = select_item.run(driver_testable)

            driver_mock.assert_called_with(select_item.css_path, select_item.hint, select_item.item_text)

            self.assertIsNone(step_result.exception)
            self.assertTrue(step_result.success)
            self.assertEqual(step_result.step, select_item)

    def test_run_select_dropdown_item_exception(self):
        exception = Exception()

        driver_testable = DriverTestable()

        select_item = SelectDropDownItemByText(ANY_CSS_PATH, ANY_HINT, ANY_TEXT)

        with patch.object(driver_testable, 'select_drop_down_item_by_text') as driver_mock:
            driver_mock.side_effect = exception

            step_result = select_item.run(driver_testable)

            driver_mock.assert_called_with(select_item.css_path, select_item.hint, select_item.item_text)

            self.assertEqual(step_result.exception, exception)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, select_item)


class TestSetCheckbox(TestCase):
    """Has unit tests for the set checkbox class"""

    def test_initializer(self):
        set_checkbox = SetCheckbox(ANY_CSS_PATH, ANY_HINT, True)

        self.assertEqual(set_checkbox.css_path, ANY_CSS_PATH)
        self.assertEqual(set_checkbox.hint, ANY_HINT)
        self.assertEqual(set_checkbox.checked, True)

    def test_run_set_checkbox(self):
        driver_testable = DriverTestable()
        set_checkbox = SetCheckbox(ANY_CSS_PATH, ANY_HINT, True)

        with patch.object(driver_testable, 'set_checkbox') as driver_mock:
            step_result = set_checkbox.run(driver_testable)

            driver_mock.assert_called_with(set_checkbox.css_path, set_checkbox.hint, set_checkbox.checked)

            self.assertEqual(step_result.step, set_checkbox)
            self.assertTrue(step_result.success)
            self.assertIsNone(step_result.exception)

    def test_run_set_checkbox_exception(self):
        driver_testable = DriverTestable()
        set_checkbox = SetCheckbox(ANY_CSS_PATH, ANY_HINT, True)

        with patch.object(driver_testable, 'set_checkbox') as driver_mock:
            exception = Exception()

            driver_mock.side_effect = exception

            step_result = set_checkbox.run(driver_testable)

            self.assertEqual(step_result.step, set_checkbox)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.exception, exception)


class TestSwitchFrame(TestCase):
    """Has unit tests for the SwitchFrame class"""

    def test_initializer(self):
        switch_frame = SwitchFrame(ANY_CSS_PATH, ANY_HINT)

        self.assertEqual(switch_frame.css_path, ANY_CSS_PATH)
        self.assertEqual(switch_frame.hint, ANY_HINT)

    def test_run(self):
        driver_testable = DriverTestable()

        switch_frame = SwitchFrame(ANY_CSS_PATH, ANY_HINT)

        with patch.object(driver_testable, 'switch_to_frame') as switch_mock:
            step_result = switch_frame.run(driver_testable)

            switch_mock.assert_called_with(switch_frame.css_path, switch_frame.hint)

            self.assertEqual(step_result.step, switch_frame)
            self.assertIsNone(step_result.exception)
            self.assertTrue(step_result.success)

    def test_run_exception(self):
        driver_testable = DriverTestable()

        switch_frame = SwitchFrame(ANY_CSS_PATH, ANY_HINT)

        exception = Exception()

        with patch.object(driver_testable, 'switch_to_frame') as switch_mock:
            switch_mock.side_effect = exception

            step_result = switch_frame.run(driver_testable)

            switch_mock.assert_called_with(switch_frame.css_path, switch_frame.hint)

            self.assertEqual(step_result.step, switch_frame)
            self.assertEqual(step_result.exception, exception)
            self.assertFalse(step_result.success)


class TestSwitchToDefaultContent(TestCase):
    """Has unit tests for the SwitchToDefaultContent class"""

    def test_run(self):
        switch_default = SwitchToDefaultContent()

        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'switch_to_default_content') as driver_mock:
            step_result = switch_default.run(driver_testable)

            self.assertTrue(driver_mock.called)
            self.assertTrue(step_result.success)
            self.assertEqual(step_result.step, switch_default)
            self.assertIsNone(step_result.exception)

    def test_run_with_exception(self):
        switch_default = SwitchToDefaultContent()

        exception = Exception()

        driver_testable = DriverTestable()

        with patch.object(driver_testable, 'switch_to_default_content') as driver_mock:
            driver_mock.side_effect = exception

            step_result = switch_default.run(driver_testable)

            self.assertTrue(driver_mock.called)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, switch_default)
            self.assertEqual(step_result.exception, exception)
