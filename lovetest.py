#!/usr/bin/env python3

import argparse
from collector import find_test_files
from runner import run_tests
from file_parser import find_functions_in_files
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

    files = args.files
    skip_files = args.skip_files
    functions = args.functions
    skip_functions = args.skip_functions

    verified_files = find_test_files(files=files, ignore=skip_files)
    function_index = find_functions_in_files(file_names=verified_files, functions=functions, ignore_functions=skip_functions)
    report = run_tests(function_index)
    print_results(report)
