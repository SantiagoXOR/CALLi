# Documentation Standards

This document outlines the standards and practices for documenting code in the Call Automation Project. Following these standards ensures consistency and completeness across the codebase.

## Core Principles

1. **Document as you develop**: Documentation should be written alongside code, not after.
2. **Keep documentation close to code**: Documentation should be as close as possible to the code it describes.
3. **Consistency matters**: Follow established patterns and templates.
4. **Audience awareness**: Consider who will read the documentation (developers, maintainers, users).
5. **Update documentation when code changes**: Documentation must be kept in sync with code.

## Documentation Types

### 1. Code Documentation

#### Python (Backend)

Use Google-style docstrings for all Python code:

```python
def function_name(param1: type, param2: type) -> return_type:
    """Short description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When and why this exception is raised
    """
    # Function implementation
```

For classes:

```python
class ClassName:
    """Short description of class.

    Longer description if needed.

    Attributes:
        attr1: Description of attr1
        attr2: Description of attr2
    """

    def __init__(self, param1: type, param2: type):
        """Initialize the class.

        Args:
            param1: Description of param1
            param2: Description of param2
        """
        self.attr1 = param1
        self.attr2 = param2
```

#### TypeScript/JavaScript (Frontend)

Use JSDoc for TypeScript/JavaScript code:

```typescript
/**
 * Short description of function
 * 
 * @param {string} param1 - Description of param1
 * @param {number} param2 - Description of param2
 * @returns {ReturnType} Description of return value
 * @throws {ErrorType} When and why this error is thrown
 */
function functionName(param1: string, param2: number): ReturnType {
    // Function implementation
}
```

For React components:

```typescript
/**
 * Component description
 * 
 * @component
 * @example
 * ```tsx
 * <ComponentName prop1="value" prop2={42} />
 * ```
 */
function ComponentName({ prop1, prop2 }: ComponentProps): JSX.Element {
    // Component implementation
}
```

### 2. Module/File Documentation

Every module/file should have a header comment explaining its purpose:

#### Python

```python
"""
Module for handling campaign-related operations.

This module provides services and utilities for creating, updating,
and managing call campaigns.
"""
```

#### TypeScript/JavaScript

```typescript
/**
 * Module for campaign management components
 * 
 * This module contains components for displaying and managing
 * call campaigns in the user interface.
 */
```

### 3. Architecture Documentation

Architecture documentation should be maintained in dedicated files:

- Backend: RST files in `backend-call-automation/docs/`
- Frontend: Markdown files in `docs/`

Update architecture documentation when making significant changes to system design.

## Documentation Review Process

1. Documentation changes should be included in the same PR as code changes
2. Code reviewers should verify documentation is:
   - Accurate and reflects the actual code behavior
   - Complete (covers all public APIs)
   - Clear and understandable
   - Follows the established standards

## Automated Documentation Checks

The CI pipeline includes checks for:
- Documentation build success
- Link validity
- Diagram validation

## Documentation Generation

- Backend: Sphinx generates HTML documentation from RST files and docstrings
- Frontend: Documentation is primarily in Markdown files

## Recommended Tools

- VS Code extensions:
  - Better Comments
  - autoDocstring (Python)
  - Document This (TypeScript/JavaScript)
- Pre-commit hooks for documentation linting
