from test_steps import Navigate
from test_steps import Click
from test_metadata import Test
from test_runner import TestRunner


test = Test()
test.add_step(Navigate('http://www.seleniumhq.org'))
test.add_step(Click(css_path='#sidebar > div.downloadBox > a',
                    hint='Download button'))

test_runner = TestRunner(test)
test_result = test_runner.run_test()

print(test_result)