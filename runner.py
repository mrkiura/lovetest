import ast
import traceback
import time
from typing import Tuple, Counter, Callable, List, Dict

from file_parser import parse_tests


def get_function_objects(test_file_name: str, functions=None) -> Tuple[dict, Counter, dict]:
    """
    Get the function objects from the test file and return them as a dictionary.
    Args:
        test_file_name (str): The name of the test file.
        functions (Optional): Optional argument for functions. Defaults to None.
    Returns:
        func_objects (Dict[str, object]): A dictionary containing function names and function objects.
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


def run_all_tests(modules: Dict[str, List[Callable]]):
    results = {}
    counter = Counter()
    errors = {}
    failures = {}

    for file_name, functions in modules.items():
        counter = Counter({key: 0 for key in ["PASS", "ERROR", "FAIL"]})
        for func_name, func in functions.items():
            try:
                start_time = time.time()
                func()
                counter["PASS"] += 1
                results[func_name] = "PASS"
                counter["PASS"] += 1
            except AssertionError as e:
                # tb_str = "".join(traceback.format_exception_only(type(e), e))
                tb_str = traceback.format_exc()
                failures[func_name] = tb_str
                counter["FAIL"] += 1
            except Exception as e:
                tb_str = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                tb_str = tb_str[tb_str.find("\n")+1:]
                errors[func_name] = tb_str
                counter["ERROR"] += 1
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                counter["ELAPSED"] += elapsed_time

    return results, counter, errors, failures


def run_test_files(file_names: list[str]) -> dict[str, Tuple[dict, Counter, dict]]:
    """Run the test files provided and return a report as a dict."""

    modules = {file_name: get_function_objects(file_name) for file_name in file_names}

    results, counter, errors, failures = run_all_tests(modules)
    return {
        "results": results,
        "errors": errors,
        "counter": counter,
        "failures": failures
    }
