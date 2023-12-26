import ast

from collections import defaultdict
from pathlib import Path


def parse_tests(
    filename: str,
    source: str = None,
) -> defaultdict[str, list]:
    """
    Parse test functions from a given source file.

    Reads the source code from the given filename or directly
    from the provided source string, parses the AST, and extracts all the
    function names that start with "test". It returns a dictionary whose values are
    function names and AST nodes.

    Usage:

    To parse test functions from a file:

        >>> results = parse_tests("path/to/your/test_file.py")

    To parse test functions from a string containing source code:

        >>> parse_tests(source="def test():assert True", filename="test.py")
        defaultdict(<class 'list'>, {'function_names': ['test'], 'nodes': [<ast.FunctionDef object at 0x104905690>]})

    Returns:
    defaultdict[str, list]
        A default dict with two keys: 'function_names' and 'nodes'
    """

    function_names = []
    try:
        if not source:
            with open(filename, "r") as file:
                source = file.read()
    except FileNotFoundError:
        raise
    tree = ast.parse(source, filename=filename)

    for node in ast.walk(tree):
        match node:
            case ast.FunctionDef(name=name) if name.startswith("test"):
                function_names.append(name)

    return function_names, tree.body
