from test_steps import *
from test_metadata import Test
from test_runner import TestRunner


def run():
    test = Test("Sample test!")
    # Navigates to Selenium's home page
    test.add_step(Navigate('http://www.seleniumhq.org'))
    # Clicks an element if it is found but does not fail if it is not
    test.add_step(ClickIfFound(css_path='#nonexistent_id', hint='An nonexistent link'))
    # Clicks the download button
    test.add_step(Click(css_path='#sidebar > div.downloadBox > a',
                        hint='Download button'))
    # Asserts that the Download link for the Python version redirects to the correct URL
    test.add_step(AssertElementAttributeValue(css_path="#mainContent > table:nth-child(13) > tbody > tr:nth-child(4) > "
                                              "td:nth-child(4) > a",
                                              hint="Download link for Python",
                                              attribute_name="href",
                                              expected_value="http://pypi.python.org/pypi/selenium"))
    # Asserts the text on the Python release date element
    test.add_step(AssertElementValue(css_path='#mainContent > table:nth-child(13) > tbody > tr:nth-child(4) > '
                                              'td:nth-child(3)',
                                     hint='Python release date',
                                     expected_value='2016-11-29'))
    # Asserts that an element is not present on the web page
    test.add_step(AssertElementNotPresent(css_path='#some_nonexistent_id', hint='An nonexistent element',
                                          wait_time=3))

    test_runner = TestRunner(test)
    test_result = test_runner.run_test()

    print(test_result)
