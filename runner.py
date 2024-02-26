import traceback

from collections import Counter
from collections import defaultdict


def run_tests(function_index: dict):
    """Execute the functions in every file from modules and report."""

    results = defaultdict(dict)
    failures = defaultdict(dict)
    errors = defaultdict(dict)
    counter = Counter({key: 0 for key in ["PASS", "ERROR", "FAIL", "TOTAL"]})
    counter["TOTAL"] += len(function_index)

    for function_name, function in function_index.items():
        callable = function["callable"]
        file_name = function["file_name"]
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

    return {
        "results": results,
        "counter": counter,
        "errors": errors,
        "failures": failures,
    }
