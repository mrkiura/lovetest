from collections import Counter
from decimal import Decimal
from typing import Dict


def print_results(report: Dict) -> None:
    if not report:
        print("Ran 0 tests")
        return
    print("Running Tests...\n")

    for file_name,  file_results in report["results"].items():
        print("\n" + "=" * 70)
        print(f"{file_name}")
        print("=" * 70)

        for test_name, test_result in file_results.items():
            if "FAIL" in test_result:
                print(f"{test_name} ... FAIL")
            elif "ERROR" in test_result:
                print(f"{test_name} ... ERROR")
            elif "PASS" in test_result:
                print(f"{test_name} ... OK")

        for test_name, error_message in report["errors"][file_name].items():
            print(
                f"\n{test_name}\n----------------------------------------------------------------------"
            )
            print(f"{error_message}\n")

        for test_name, error_message in report["failures"][file_name].items():
            print(
                f"\n{test_name}\n----------------------------------------------------------------------"
            )
            print(f"{error_message}\n")

    print("PASSED (passed=" + str(results["counter"]["PASSED"]) + ")")
    print("FAILED (failures=" + str(results["counter"]["FAILED"]) + ")")


# Sample results:

results = {
    "results": {
        "test_parse_tests_with_source_string": "PASS",
        "test_parse_tests_from_file": "PASS",
        "test_parse_tests_file_not_found_raises": "PASS",
    },
    "errors": {},
    "counter": Counter(
        {"PASS": 6, "ELAPSED": 0.0011527538299560547, "ERROR": 0, "FAIL": 0}
    ),
    "failures": {},
}

expected_results = {
    "tests/test_parser.py": {
            "test_parse_tests_with_source_string": {"result": "PASS"},
            "test_parse_tests_from_file": {"result": "PASS"},
            "test_parse_tests_file_not_found_raises": {"result": "FAIL"},
        },
}
