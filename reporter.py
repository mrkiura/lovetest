from collections import Counter
from decimal import Decimal
from typing import Dict


def print_results(report: Dict) -> None:
    if not report:
        print("Ran 0 tests")
        return
    print("Running Tests...\n")

    for file_name, file_results in report["results"].items():
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
                f"\nERROR: {test_name}\n----------------------------------------------------------------------"
            )
            print(f"{error_message}\n")

        for test_name, error_message in report["failures"][file_name].items():
            print(
                f"\nFAIL: {test_name}\n----------------------------------------------------------------------"
            )
            print(f"{error_message}\n")

    print()
    print("PASS: " + str(report["counter"]["PASS"]))
    print("FAIL: " + str(report["counter"]["FAIL"]))
    print("ERROR: " + str(report["counter"]["ERROR"]))
