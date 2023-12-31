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
