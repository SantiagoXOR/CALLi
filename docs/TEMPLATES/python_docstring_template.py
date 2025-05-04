"""
Module for [brief description of module purpose].

This module provides [detailed description of module functionality and purpose].

Example:
    ```python
    from module_name import SomeClass

    instance = SomeClass(param1="value")
    result = instance.some_method()
    ```
"""

from typing import Any


class SampleClass:
    """Short description of class.

    Longer description with more details about what this class does,
    its purpose, and any important implementation details.

    Attributes:
        attr1 (type): Description of attr1
        attr2 (type): Description of attr2
    """

    def __init__(self, param1: str, param2: int | None = None):
        """Initialize the class.

        Args:
            param1: Description of param1
            param2: Description of param2, defaults to None
        """
        self.attr1 = param1
        self.attr2 = param2

    def method_name(self, param1: str, param2: int) -> dict[str, Any]:
        """Short description of method.

        Longer description with more details about what this method does,
        its purpose, and any important implementation details.

        Args:
            param1: Description of param1
            param2: Description of param2

        Returns:
            A dictionary containing the following keys:
                - key1: Description of key1's value
                - key2: Description of key2's value

        Raises:
            ValueError: When param1 is empty
            TypeError: When param2 is negative
        """
        # Method implementation


def function_name(param1: str, param2: list[int]) -> bool:
    """Short description of function.

    Longer description with more details about what this function does,
    its purpose, and any important implementation details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is empty
    """
    # Function implementation
