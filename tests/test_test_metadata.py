from unittest import TestCase
from test_metadata import Test
from tests.test_data import any_click


class TestTest(TestCase):
    """Has unit tests for the Test class"""

    def test_add_step(self):
        test = Test()

        for i in range(10):
            test.add_step(any_click())

        self.assertEqual(len(test.steps), 10)

    def test_init(self):
        test_id = 'some id for the test'

        test = Test(test_id)

        self.assertEqual(test_id, test.test_id)
