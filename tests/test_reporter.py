from collections import Counter
import io
import sys

from reporter import print_results
from unittest.mock import mock_open, patch
from file_parser import find_functions_in_files
from runner import run_tests


def capture_print_output(func, *args, **kwargs):
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = original_stdout


def test_empty_report():
    report = {}
    result = capture_print_output(print_results, report)
    assert "Ran 0 tests" in result


def test_all_passing():
    source = """
def test_pass_1():
    assert True

def test_pass_2():
    assert True
    """
    m = mock_open(read_data=source)

    with patch("builtins.open", m), patch("pathlib.Path.exists", return_value=True):
        modules = find_functions_in_files(["test_01"])
        report = run_tests(modules)
        result = capture_print_output(print_results, report)
        assert "test_pass_1 ... OK" in result


def test_mixed_results():
    source = """
def test_fail():
    raise AssertionError()

def test_error():
    raise Exception()

def test_pass():
    assert True
    """
    m = mock_open(read_data=source)

    with patch("builtins.open", m), patch("pathlib.Path.exists", return_value=True):
        modules = find_functions_in_files(["test_01"])
        report = run_tests(modules)
        result = capture_print_output(print_results, report)
        assert "test_fail ... FAIL" in result
        assert "test_error ... ERROR" in result
        assert "test_pass ... OK" in result
        assert "ERROR: test_error" in result
        assert "FAIL: test_fail" in result


def test_no_passing_tests():
    source = """
def test_fail():
    raise AssertionError()

def test_error():
    raise Exception()
    """
    m = mock_open(read_data=source)

    with patch("builtins.open", m), patch("pathlib.Path.exists", return_value=True):
        modules = find_functions_in_files(["test_01"])
        report = run_tests(modules)
        result = capture_print_output(print_results, report)
        assert "test_fail ... FAIL" in result
        assert "test_error ... ERROR" in result
        assert "ERROR: test_error" in result
        assert "FAIL: test_fail" in result

def test_stress():
    raise Exception()


def test_stress222():
    raise AssertionError()
