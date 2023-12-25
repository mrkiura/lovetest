import glob

from typing import List


def find_test_files(*files) -> List[str]:
    """
    Find test files in the project directory.

    This function searches for test files matching the given file patterns.
    If no patterns are provided, it defaults to finding all files that
    start with 'test' and end with '.py'.

    Args:
        *files: Variable length tuple of file patterns to match.

    Returns:
        A list of strings, where each string is a path to a test file
        that matched the given patterns.

    Raises:
        FileNotFoundError: If no files matched any of the given patterns.
    Usage:
        >>> all_test_files = find_test_files()
        >>> print(all_test_files)
        >>> ['tests/test_api_utils.py', 'tests/test_api_core.py', 'tests/test_models_user.py']

        >>> specific_test_files = find_test_files('test_api_*.py')
        >>> print(specific_test_files)
        >>> ['tests/test_api_core.py', 'tests/test_api_utils.py']
    """

    test_files = []

    if files:
        for file in files:
            matches = glob.glob(f"**/{file}", recursive=True)
            test_files.extend(matches)
    else:
        test_files = glob.glob("**/test*.py", recursive=True)

    if not test_files:
        raise FileNotFoundError("No files matched any of the given patterns.")

    return test_files
