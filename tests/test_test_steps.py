from unittest import TestCase
from tests.testables import DriverTestable
from tests.test_data import *
from test_steps import *
from mock import patch


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


class TestAssertAttributeValue(TestCase):
    """"Has unit tests for the AssertAttributeValue class"""

    def test_initializer(self):
        assert_attribute = AssertAttributeValue(ANY_CSS_PATH, ANY_HINT, ANY_ATTRIBUTE_NAME, ANY_VALUE)

        self.assertEqual(assert_attribute.css_path, ANY_CSS_PATH)
        self.assertEqual(assert_attribute.hint, ANY_HINT)
        self.assertEqual(assert_attribute.attribute_name, ANY_ATTRIBUTE_NAME)
        self.assertEqual(assert_attribute.expected_value, ANY_VALUE)

    def test_run_assert_attribute(self):
        driver_testable = DriverTestable()

        assert_attribute = any_assert_attribute()

        with patch.object(driver_testable, 'get_element_attribute', return_value=assert_attribute.expected_value) \
                as assert_value_mock:
            assert_attribute = any_assert_attribute()

            step_result = assert_attribute.run(driver_testable)

            assert_value_mock.assert_called_with(assert_attribute.css_path, assert_attribute.hint,
                                                 assert_attribute.attribute_name, assert_attribute.expected_value)
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
                                                 assert_attribute.attribute_name, assert_attribute.expected_value)

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
                                                 assert_attribute.attribute_name, assert_attribute.expected_value)
            self.assertFalse(step_result.success)
            self.assertEqual(step_result.step, assert_attribute)
            self.assertEqual(step_result.exception, exception)
