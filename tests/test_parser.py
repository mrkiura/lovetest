import ast
from unittest.mock import mock_open, patch
from utils import assert_raises

from file_parser import parse_files


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

    function_names, nodes = parse_files(filename="test.py", source=source)

    assert "test_func_one" in function_names
    assert "test_func_two" in function_names
    assert len(function_names) == 2
    assert any(
        isinstance(node, ast.FunctionDef) for node in nodes
    ), "No function defined"


def test_parse_tests_from_file():
    m = mock_open(read_data=MOCK_SOURCE_CODE)

    with patch("builtins.open", m), patch("pathlib.Path.exists", return_value=True):
        function_names, nodes = parse_files(filename=MOCK_FILE_PATH)

        m.assert_called_once_with(MOCK_FILE_PATH, "r")
        assert "test_func_one" in function_names
        assert "test_func_two" in function_names
        assert len(function_names) == 2
        assert any(
            isinstance(node, ast.FunctionDef) for node in nodes
        ), "No function defined"
        # assert [in] in nodes


def test_parse_tests_file_not_found_raises():
    with assert_raises(FileNotFoundError):
        parse_files(filename="temp_file_name")
