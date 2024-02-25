import ast
import traceback

from collections import defaultdict
from typing import Counter, Callable, List

from file_parser import parse_tests


def get_function_objects(test_file_name: str, functions=None) -> List[Callable]:
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

    func_objects = [global_context[func_name] for func_name in function_names]

    return func_objects


def run_tests(file_names: list[str]):
    """Execute the functions in every file from file names and report."""

    modules = {file_name: get_function_objects(file_name) for file_name in file_names}

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
            except AssertionError:
                tb_str = traceback.format_exc()
                results[file_name][function_name] = "FAIL"
                failures[file_name][function_name] =  tb_str
                counter["FAIL"] += 1
            except Exception as e:
                tb_str = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                tb_str = tb_str[tb_str.find("\n")+1:]
                results[file_name][function_name] = "ERROR"
                errors[file_name][function_name] =  tb_str
                counter["ERROR"] += 1
            else:
                counter["PASS"] += 1
                results[file_name][function_name] = "PASS"
                counter["PASS"] += 1

    return {
        "results": results,
        "counter": counter,
        "errors": errors,
        "failures": failures
    }
