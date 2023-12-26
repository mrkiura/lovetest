import ast
import traceback
from typing import Tuple, Counter
from file_parser import parse_tests
import time


def run_test_file(test_file_name: str) -> Tuple[dict, Counter, dict]:
    """Run the test functions defined in a file.

    Args:
        test_file_name (str): Name of file

    Returns:
        Tuple[Dict, Counter, Dict]: _description_
    """
    with open(test_file_name, "r") as test_file:
        source = test_file.read()

    results = {}
    counter = Counter()
    errors = {}
    failures = {}
    global_context = {}

    function_names, nodes = parse_tests(source=source, filename=test_file_name)

    module = ast.Module(body=nodes)
    code = compile(source=module, filename=test_file_name, mode="exec")
    exec(code, global_context)

    for function in function_names:
        try:
            start_time = time.time()
            exec(f"{function}()", global_context)
            end_time = time.time()
            elapsed_time = end_time - start_time
            results[function] = "PASS"
            counter["PASS"] += 1
        except AssertionError:
            error_message = traceback.format_exc()
            results[function] = "FAIL"
            counter["FAIL"] += 1
            failures[function] = error_message
        except Exception:
            error_message = traceback.format_exc()
            results[function] = f"ERROR: {error_message}"
            errors[function] = error_message
            counter["ERROR"] += 1

        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            counter["ELAPSED"] += elapsed_time

    return results, counter, errors, failures


def run_test_files(test_files: list[str]) -> dict[str, Tuple[dict, Counter, dict]]:
    """Run the test files provided and return a report as a dict.

    Args:
        test_files (list[str]): _description_

    Returns:
        dict[str, Tuple[dict, Counter, dict]]: _description_

    """
    report = dict()

    for test_file_name in test_files:
        report[test_file_name] = run_test_file(test_file_name)

    return report