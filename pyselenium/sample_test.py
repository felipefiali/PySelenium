from pyselenium.test_metadata import Test
from pyselenium.test_steps import *
from pyselenium.test_runner import TestRunner


if __name__ == "__main__":
    test = Test('Sample test')
    # Navigates to Selenium's home page
    test.add_step(Navigate('http://www.seleniumhq.org'))
    # Clicks an element if it is found but does not fail if it is not
    test.add_step(ClickIfFound(css_path='#nonexistent_id', hint='An nonexistent link', wait_time=2))
    # Clicks the download button
    test.add_step(Click(css_path='#sidebar > div.downloadBox > a',
                        hint='Download button'))
    # Asserts that the Download link for the Python version redirects to the correct URL
    test.add_step(AssertElementAttributeValue(css_path='#mainContent > table:nth-child(13) > tbody > tr:nth-child(4) > '
                                              'td:nth-child(4) > a',
                                              hint='Download link for Python',
                                              attribute_name='href',
                                              expected_value='http://pypi.python.org/pypi/selenium'))
    # Asserts the text on the Python release date element
    test.add_step(AssertElementValue(css_path='#mainContent > table:nth-child(13) > tbody > tr:nth-child(4) > '
                                              'td:nth-child(3)',
                                     hint='Python release date',
                                     expected_value='2016-11-29'))
    # Asserts that an element is not present on the web page
    test.add_step(AssertElementNotPresent(css_path='#some_nonexistent_id', hint='An nonexistent element',
                                          wait_time=3))
    # Sends text to the search input element
    test.add_step(TypeText(css_path='#q', hint='Search selenium input', text='Searching selenium!'))
    # Simulates the user pressing the return button on the keyboard
    test.add_step(SendEnter())
    test.add_step(Navigate('http://www.seleniumhq.org/sponsor/'))
    # Selects an option inside a select element
    test.add_step(SelectDropDownItemByText(css_path='#mainContent > form > table > tbody > tr:nth-child(2) >'
                                                    ' td > select',
                                           hint='Sponsor options',
                                           item_text='Bronze Sponsor $500.00 USD'))
    test.add_step(Navigate('http://www.w3schools.com/html/tryit.asp?filename=tryhtml_checkbox'))
    # Switches to an iFrame on the page
    test.add_step(SwitchFrame(css_path='#iframeResult',
                              hint='Result iFrame'))
    # Checks and unchecks a checkbox on the page
    test.add_step(SetCheckbox(css_path='body > form > input[type="checkbox"]:nth-child(1)',
                              hint='I have a bike',
                              checked=True))
    test.add_step(SetCheckbox(css_path='body > form > input[type="checkbox"]:nth-child(3)',
                              hint='I have a car',
                              checked=False))
    test.add_step(SetCheckbox(css_path='body > form > input[type="checkbox"]:nth-child(1)',
                              hint='I have a bike',
                              checked=False))
    # Switches the context to the default content. Necessary to use after switching to a specific iFrame.
    test.add_step(SwitchToDefaultContent())

    # Runs the test and prints the result
    test_runner = TestRunner(test)
    test_result = test_runner.run_test()

    print(test_result)
