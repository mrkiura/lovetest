import pytest
from unittest.mock import mock_open, patch
from file_parser import parse_tests


MOCK_SOURCE_CODE = """
def test_func_one():
    assert True

def test_func_two():
    assert False

def not_a_test():
    pass
"""

MOCK_FILE_PATH = "path/to/tests/test_file.py"


def test_parse_tests_with_source_string():
    source = MOCK_SOURCE_CODE

    results = parse_tests(filename="test.py", source=source)

    assert "test_func_one" in results["function_names"]
    assert "test_func_two" in results["function_names"]
    assert len(results["function_names"]) == 2
    assert len(results["nodes"]) > 0


def test_parse_tests_from_file():
    m = mock_open(read_data=MOCK_SOURCE_CODE)

    with patch("builtins.open", m), patch("pathlib.Path.exists", return_value=True):
        results = parse_tests(filename=MOCK_FILE_PATH)

        m.assert_called_once_with(MOCK_FILE_PATH, "r")
        assert "test_func_one" in results["function_names"]
        assert "test_func_two" in results["function_names"]
        assert len(results["function_names"]) == 2
        assert len(results["nodes"]) > 0


def test_parse_tests_file_not_found():
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            parse_tests(filename=MOCK_FILE_PATH)
