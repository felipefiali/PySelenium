from unittest import TestCase
from test_metadata import Test
from test_steps import Click


class TestTest(TestCase):
    """Has unit tests for the Test class"""

    def test_add_step_counter(self):
        test = Test()
        self.assertEqual(test.currentStepCounter, 0)

        step = Click()
        test.add_step(step)
        self.assertEqual(test.currentStepCounter, 1)

        self.assertEqual(step.order, 1)

    def test_add_step(self):
        test = Test()

        for i in range(10):
            test.add_step(Click())

        self.assertEqual(len(test.steps), 10)