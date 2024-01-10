import ast
import traceback
from typing import Tuple, Counter, List
from file_parser import parse_tests



def get_function_objects(test_file_name: str, functions=None) -> Tuple[dict, Counter, dict]:
    """
    Get the function objects from the test file and return them as a dictionary.
    Args:
        test_file_name (str): The name of the test file.
        functions (Optional): Optional argument for functions. Defaults to None.
    Returns:
        Tuple[dict, Counter, dict]: A tuple containing the function objects, counter, and errors.
    """
    with open(test_file_name, "r") as test_file:
        source = test_file.read()

    global_context = {}

    function_names, nodes = parse_tests(source=source, filename=test_file_name)

    module = ast.Module(body=nodes)
    code = compile(source=module, filename=test_file_name, mode="exec")
    exec(code, global_context)

    func_objects = {func_name: global_context[func_name] for func_name in function_names}

    return func_objects


def run_all_tests(modules: dict):
    results = {}
    errors = {}
    for file_name, functions in modules.items():
        counter = Counter({key: 0 for key in ["PASS", "ERROR", "FAIL"]})
        for func_name, func in functions.items():
            try:
                func()
                counter["PASS"] += 1
            except AssertionError:
                errors[func_name] = traceback.format_exc()
                counter["FAIL"] += 1
            except Exception:
                errors[func_name] = traceback.format_exc()
                counter["ERROR"] += 1
        results[file_name] = counter

    return results, errors


def run_test_files(file_names: list[str]) -> dict[str, Tuple[dict, Counter, dict]]:
    """Run the test files provided and return a report as a dict."""

    modules = {file_name: get_function_objects(file_name) for file_name in file_names}

    results, errors = run_all_tests(modules)
    return {
        "results": results,
        "errors": errors
    }
