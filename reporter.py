from collections import Counter
from typing import Dict


def print_results(report: Dict) -> None:
    print("Test results.\n")

    summary = Counter()
    for test_file, (results, counter, errors, failures) in report.items():
        print("\n" + "=" * 70)
        print(f"{test_file}")
        print("=" * 70)
        summary["PASS"] += counter["PASS"]
        summary["FAIL"] += counter["FAIL"]
        summary["ERROR"] += counter["ERROR"]
        summary["ELAPSED"] += counter["ELAPSED"]
        for test_name, test_result in results.items():
            summary["COUNT"] += 1
            if "FAIL" in test_result:
                print(f"{test_name} ... FAIL")
            elif "ERROR" in test_result:
                print(f"{test_name} ... ERROR")
            elif "PASS" in test_result:
                print(f"{test_name} ... OK")

        for test_name, error_message in errors.items():
            print(
                f"ERROR: {test_name}\n----------------------------------------------------------------------"
            )
            print(f"{error_message}\n")

        for test_name, error_message in failures.items():
            print(
                f"FAIL: {test_name}\n----------------------------------------------------------------------"
            )
            print(f"{error_message}\n")

    print(f"\nRan {summary['COUNT']} tests\n")
    print("PASS (pass=" + str(summary["PASS"]) + ")")
    print("FAIL (fail=" + str(summary["FAIL"]) + ")")
    print("ERROR (error=" + str(summary["ERROR"]) + ")")
