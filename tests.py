"""Basic output validation tests"""

import urbandict


# pytest
extra_plugin_dir = '.'
pytest_plugins = ['errbot.backends.test']



def test_with_no_arguments(testbot):
    testbot.push_message('!ud')
    result = testbot.pop_message()
    assert result is not None


def test_with_argument(testbot):
    term = 'ahlie'
    testbot.push_message('!ud ' + term)
    result = testbot.pop_message()
    assert term in result


def test_without_argument(testbot):
    term = 'imnotactuallyaword'
    testbot.push_message('!ud ' + term)
    result = testbot.pop_message()
    assert "No such term: " + term in result