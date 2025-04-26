#!/usr/bin/env python
"""
Script to check Python docstrings for compliance with project standards.

This script validates that Python files have proper docstrings at module,
class, method, and function levels according to the Google docstring style.
"""

import ast
import os
import sys
from typing import List, Set, Tuple


def check_docstrings(filename: str) -> List[str]:
    """Check docstrings in a Python file.

    Args:
        filename: Path to the Python file to check

    Returns:
        List of error messages, empty if no errors
    """
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    errors = []
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return [f"Syntax error in {filename}: {e}"]

    # Check module docstring
    if not ast.get_docstring(tree):
        errors.append(f"Missing module docstring in {filename}")

    # Check classes and functions
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip private methods/functions (starting with _)
            if node.name.startswith('_') and node.name != '__init__':
                continue
                
            docstring = ast.get_docstring(node)
            if not docstring:
                errors.append(f"Missing docstring for {node.__class__.__name__} '{node.name}' in {filename}")
            elif docstring and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Check function docstring sections
                if "Args:" not in docstring and "Parameters:" not in docstring and len(node.args.args) > 1:
                    # First arg might be self/cls, so only warn if more than 1 arg
                    errors.append(f"Function '{node.name}' in {filename} is missing Args: section")
                
                if "Returns:" not in docstring and node.returns:
                    errors.append(f"Function '{node.name}' in {filename} has return annotation but missing Returns: section")

    return errors


def main() -> int:
    """Run the docstring checker on specified files.

    Returns:
        Exit code (0 for success, 1 for errors)
    """
    files = sys.argv[1:]
    if not files:
        print("No files to check")
        return 0

    all_errors = []
    for filename in files:
        if filename.endswith('.py'):
            errors = check_docstrings(filename)
            all_errors.extend(errors)

    for error in all_errors:
        print(error)

    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
