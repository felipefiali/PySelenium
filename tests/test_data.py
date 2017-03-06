from pyselenium.test_steps import AssertElementAttributeValue
from pyselenium.test_steps import Click
from pyselenium.test_steps import Navigate

ANY_CSS_PATH = 'any css path'
ANY_HINT = 'any hint'
ANY_URL = 'any url'
ANY_ATTRIBUTE_NAME = 'any attribute name'
ANY_VALUE = 'foo bar'
ANY_TEXT = ANY_VALUE
ANY_OTHER_VALUE = ANY_URL
ANY_WAIT_TIME = 1


def any_click():
    return Click(ANY_CSS_PATH, ANY_HINT)


def any_navigate():
    return Navigate(ANY_URL)


def any_assert_attribute():
    return AssertElementAttributeValue(ANY_CSS_PATH, ANY_HINT, ANY_ATTRIBUTE_NAME, ANY_VALUE)
