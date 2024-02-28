import ast

import typing as tp

from collections import ChainMap
from utils import get_source


def parse_files(
    file_name: str,
    source: tp.Optional[str] = None,
) -> tp.Tuple[tp.Sequence[str], tp.Sequence[ast.AST]]:
    """
    Parse test function names from a given source file or string.

    Reads the source code from the provided file_name or directly from the given source string,
    parses the AST (Abstract Syntax Tree), and extracts the names of all functions that start with "test".

    It returns a tuple containing a list of function names and a list of AST nodes corresponding to the body of the module.

    Usage:

    To parse test function names from a file:

        >>> function_names, _ = parse_files("path/to/your/test_file.py")
        >>> function_names
        ['test_function1', 'test_function2']

    To parse test function names from a string containing source code:

        >>> function_names, _ = parse_files(source="def test_function(): assert True", file_name="test.py")
        >>> function_names
        ['test_function']

    Returns:
    Tuple[Sequence[str], Sequence[ast.AST]]
        Function names and ast nodes representing module body.
    """

    function_names: list = []
    try:
        if not source:
            source = get_source(file_name)
    except FileNotFoundError:
        raise

    tree = ast.parse(source, filename=file_name)

    for node in ast.walk(tree):
        match node:
            case ast.FunctionDef(name=name) if name.startswith("test"):
                function_names.append(name)

    return function_names, tree.body


def find_functions_in_file(test_file_name: str) -> tp.Dict[str, dict]:
    """
    Get the function objects from the test file and return them as a list.
    Args:
        test_file_name (str): The name of the test file.
        functions (Optional): Optional argument for functions. Defaults to None.
    Returns:
        func_objects (List[Callable]): A list of function objects.
    """
    source = get_source(test_file_name)

    global_context = {}

    function_names, nodes = parse_files(source=source, file_name=test_file_name)

    module = ast.Module(body=nodes)
    code = compile(source=module, filename=test_file_name, mode="exec")
    exec(code, global_context)

    func_objects = {
        func_name: {"callable": global_context[func_name], "file_name": test_file_name}
        for func_name in function_names
    }

    return func_objects


def find_functions_in_files(
    file_names: tp.List[str], functions=None, ignore=None
) -> dict:
    """Fetch all functions for each file name.

    Args:
        file_names (tp.List[str]): List of files to collect functions from
        functions (tp.List[str], optional): If provided, only collect functions in this list.
        ignore (tp.List[str], optional): If provided, do not collect any function on this list.

    Returns:
        dict: A key value mapping where keys are function names and values are dicts with the keys callable and file name.
    """
    func_objects_list = [find_functions_in_file(file_name) for file_name in file_names]
    func_index = dict(ChainMap(*func_objects_list))

    if functions:
        func_index = {
            func_name: func_index[func_name]
            for func_name in functions
            if func_name in func_index
        }

    if ignore:
        for func_name in ignore:
            func_index.pop(func_name, None)

    return func_index
