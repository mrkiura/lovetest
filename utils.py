from collections import Counter
import traceback
import ast


class assert_raises:
    """
    A context manager to assert that a specific exception is raised.

    This context manager is used in tests to ensure that a certain exception is
    raised within a block of code. If the expected exception is not raised,
    the test will fail.

    Attributes:
        exception_type (Type[Exception]): The type of the exception expected to be raised.

    Usage example:
        with assert_raises(ValueError):
            raise ValueError("An expected error occurred")
    """

    def __init__(self, exception_type) -> None:
        self.exception_type = exception_type

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        assert exc_type == self.exception_type, "No expected Exceptions raised."
        return True


def ast_to_func(node):
    """
    Convert an ast.FunctionDef object to a code object.
    """
    node = ast.fix_missing_locations(node)

    module = ast.Module(body=[node], type_ignores=[])
    code_obj = compile(module, '<string>', 'exec')

    context = {}
    exec(code_obj, context)
    return context[node.name]


def get_source(filename: str) -> str:
    with open(filename, "r") as file:
        source = file.read()
    return source
