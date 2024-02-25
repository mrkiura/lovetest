from collections import Counter
import io
import sys

from reporter import print_results
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
    report = {
        "test_file_01": (
            {"test_pass_01": "PASS"},
            Counter({"PASS": 1, "FAIL": 0, "ERROR": 0, "ELAPSED": 0.1}),
            {},
            {},
        )
    }
    result = capture_print_output(print_results, report)
    assert "test_pass_01 ... OK" in result


def test_mixed_results():
    report = {
        "test_file_01": (
            {"test_pass_01": "PASS", "test_fail_01": "FAIL", "test_error_01": "ERROR"},
            Counter({"PASS": 1, "FAIL": 1, "ERROR": 1, "ELAPSED": 0.3}),
            {"test_error_01": "An error occurred."},
            {"test_fail_01": "AssertionError"},
        )
    }
    result = capture_print_output(print_results, report)
    assert "test_fail_01 ... FAIL" in result
    assert "test_error_01 ... ERROR" in result
    assert "ERROR: test_error_01" in result
    assert "FAIL: test_fail_01" in result


def test_no_passing_tests():
    report = {
        "test_file_01": (
            {"test_fail_01": "FAIL", "test_error_01": "ERROR"},
            Counter({"PASS": 0, "FAIL": 1, "ERROR": 1, "ELAPSED": 0.2}),
            {"test_error_01": "An error occurred."},
            {"test_fail_01": "AssertionError"},
        )
    }
    result = capture_print_output(print_results, report)
    assert "test_fail_01 ... FAIL" in result
    assert "test_error_01 ... ERROR" in result
    assert "test_pass_01 ... OK" not in result


def test_assert_fail():
    name = 20
    raise AssertionError("Big L")
