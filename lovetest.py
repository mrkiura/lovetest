#!/usr/bin/env python3

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run specific Python tests or test files."
    )
    parser.add_argument("--files", nargs="*", help="Specify test files to run.")
    parser.add_argument("--skip-files", nargs="*", help="Specify test files to skip.")
    parser.add_argument("--functions", nargs="*", help="Specify test functions to run.")
    parser.add_argument("--skip-functions", nargs="*", help="Specify test functions to skip.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    match args.__dict__:
        case {"files": list(files)} if len(files) > 0:
            print(f"files {files}")
        case {"skip_files": list(files)} if len(files) > 0:
            print(f"files {files}")
        case {"functions": list(functions)} if len(functions) > 0:
            print(f"functions {functions}")
        case {"skip_functions": list(functions)} if len(functions) > 0:
            print(f"functions {functions}")
        case _:  # default, run all tests.
            print("No args, running all tests")
