import ast
import traceback

from pprint import pprint
from collections import defaultdict
from typing import Counter, Callable, List

from file_parser import parse_files


def find_functions(test_file_name: str, functions=None) -> List[Callable]:
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

    function_names, nodes = parse_files(source=source, filename=test_file_name)

    module = ast.Module(body=nodes)
    code = compile(source=module, filename=test_file_name, mode="exec")
    exec(code, global_context)

    func_objects = [global_context[func_name] for func_name in function_names]

    return func_objects


def run_tests(modules):
    """Execute the functions in every file from modules and report."""

    results = defaultdict(dict)
    failures = defaultdict(dict)
    errors = defaultdict(dict)
    counter = Counter()

    for file_name, callables in modules.items():
        counter = Counter({key: 0 for key in ["PASS", "ERROR", "FAIL"]})
        for callable in callables:
            function_name = callable.__name__
            try:
                callable()
            except AssertionError as e:
                tbs = traceback.format_exception(type(e), e, e.__traceback__)
                del tbs[1]
                tb_str = "".join(tbs)
                results[file_name][function_name] = "FAIL"
                failures[file_name][function_name] = tb_str
                counter["FAIL"] += 1
            except Exception as e:
                tbs = traceback.format_exception(type(e), e, e.__traceback__)
                del tbs[1]
                tb_str = "".join(tbs)
                results[file_name][function_name] = "ERROR"
                errors[file_name][function_name] = tb_str
                counter["ERROR"] += 1
            else:
                counter["PASS"] += 1
                results[file_name][function_name] = "PASS"
                counter["PASS"] += 1

    return {
        "results": results,
        "counter": counter,
        "errors": errors,
        "failures": failures,
    }
