from test_steps import Navigate
from test_steps import Click
from test_steps import AssertAttributeValue
from test_metadata import Test
from test_runner import TestRunner


def run():
    test = Test("Sample test!")
    # Navigates to Selenium's home page
    test.add_step(Navigate('http://www.seleniumhq.org'))
    # Clicks the download button
    test.add_step(Click(css_path='#sidebar > div.downloadBox > a',
                        hint='Download button'))
    # Asserts that the Download link for the Python version redirects to the correct URL
    test.add_step(AssertAttributeValue(css_path="#mainContent > table:nth-child(13) > tbody > tr:nth-child(4) > "
                                                "td:nth-child(4) > a",
                                       hint="Download link for Python",
                                       attribute_name="href",
                                       expected_value="http://pypi.python.org/pypi/selenium"))

    test_runner = TestRunner(test)
    test_result = test_runner.run_test()

    print(test_result)
