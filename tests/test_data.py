from test_steps import Click
from test_steps import Navigate


ANY_CSS_PATH = 'any css path'
ANY_HINT = 'any hint'
ANY_URL = 'any url'


def any_click():
    return Click(ANY_CSS_PATH, ANY_HINT)

def any_navigate():
    return Navigate(ANY_URL)
