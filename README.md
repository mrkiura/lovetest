# lovetest

lovetest is a Python test runner designed to simplify the process of running and reporting on unit tests. It allows you to specify which test files or functions to run, and which to skip.

## Features

- Run specific test files or individual test functions.
- Skip specific test files or individual test functions.
- Detailed test reports including pass, fail, and error counts.

## Installation

Coming soon after pypi publishing

## Usage

How to use lovetest, including command-line arguments.

When passing file names as options to lovetest, you do not need to include the full path, just the file name.

So instead of passing `tests/test_api.py` to the command line args, passing `test_api.py` will be sufficient.

```bash
bash
./lovetest.py --files test_file1.py test_file2.py
./lovetest.py --skip-files test_file3.py
./lovetest.py --functions test_func1 test_func2
./lovetest.py --skip-functions test_func3
```

## Test Files

Tests should be located in the same folder that lovetest will be run from. Tests can be organized as follows:

- A python file whose name is prefixed with `test`
- A directory whose name is prefixed with `test`. The directory may contain subdirectories. As long as the test files inside the directories are named beginning with `test`. They will be automatically discovered unless explicitly skipped by passing the --skip-files command line args.

## Reporting

Lovetest publishes the test results to the terminal.

A sample report looks like this.

```bash
Test results.


======================================================================
tests/test_reporter.py
======================================================================
test_empty_report ... OK
test_all_passing ... OK
test_mixed_results ... OK
test_no_passing_tests ... OK

======================================================================
tests/test_parser.py
======================================================================
test_parse_tests_with_source_string ... OK
test_parse_tests_from_file ... OK
test_parse_tests_file_not_found_raises ... OK

Ran 7 tests

PASS (pass=7)
FAIL (fail=0)
ERROR (error=0)
```

## License

lovetest is MIT licensed, as found in the LICENSE file.
