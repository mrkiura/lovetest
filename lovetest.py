#!/usr/bin/env python3

import argparse
from collector import find_test_files
from runner import run_test_files
from reporter import print_results


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run specific Python tests or test files."
    )
    parser.add_argument("--files", nargs="*", help="Specify test files to run.")
    parser.add_argument("--skip-files", nargs="*", help="Specify test files to skip.")
    parser.add_argument("--functions", nargs="*", help="Specify test functions to run.")
    parser.add_argument(
        "--skip-functions", nargs="*", help="Specify test functions to skip."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    match args.__dict__:
        case {"files": list(files)} if len(files) > 0:
            verified_files = find_test_files(*files)
            report = run_test_files(verified_files)
            print_results(report)

        case {"skip_files": list(files)} if len(files) > 0:
            verified_files = find_test_files(ignore=files)
            report = run_test_files(verified_files)
            print_results(report)
        case {"functions": list(functions)} if len(functions) > 0:
            verified_files = find_test_files()
            report = run_test_files(verified_files)
            print_results(report)
        case {"skip_functions": list(functions)} if len(functions) > 0:
            verified_files = find_test_files()
            report = run_test_files(verified_files)
            print_results(report)
        case _:  # default, run all tests.
            verified_files = find_test_files()
            report = run_test_files(verified_files)
            print_results(report)
