# Documentation as Code

This guide outlines our approach to treating documentation as code in the Call Automation Project.

## Core Principles

1. **Documentation is code**: Documentation is treated with the same care and rigor as code
2. **Version control**: Documentation lives in the same repository as code
3. **Automated validation**: Documentation is automatically validated
4. **Continuous integration**: Documentation is built and deployed automatically
5. **Review process**: Documentation changes are reviewed like code changes

## Documentation Types and Locations

### Code Documentation

Code documentation lives directly in the source code:

- **Python**: Google-style docstrings
- **TypeScript/JavaScript**: JSDoc comments

Example Python docstring:
```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is empty
    """
    # Function implementation
```

Example TypeScript JSDoc:
```typescript
/**
 * Short description of function
 *
 * @param {string} param1 - Description of param1
 * @param {number} param2 - Description of param2
 * @returns {boolean} Description of return value
 * @throws {Error} When param1 is empty
 */
function functionName(param1: string, param2: number): boolean {
    // Function implementation
}
```

### Architecture Documentation

Architecture documentation lives in dedicated files:

- **Backend**: RST files in `backend-call-automation/docs/`
- **Frontend**: Markdown files in `docs/`

### User Documentation

User documentation lives in dedicated files:

- Markdown files in `docs/user-guides/`

## Documentation Lifecycle

Documentation follows the same lifecycle as code:

1. **Creation**: Documentation is created alongside code
2. **Review**: Documentation is reviewed alongside code
3. **Versioning**: Documentation is versioned alongside code
4. **Deployment**: Documentation is deployed alongside code
5. **Maintenance**: Documentation is maintained alongside code

## Documentation Tools

We use the following tools for documentation:

- **Sphinx**: For building backend documentation
- **Markdown**: For frontend and general documentation
- **PlantUML**: For diagrams
- **Pre-commit hooks**: For validating documentation
- **GitHub Actions**: For building and deploying documentation

## Documentation Review Checklist

When reviewing documentation, check for:

- **Accuracy**: Does the documentation accurately describe the code?
- **Completeness**: Does the documentation cover all necessary aspects?
- **Clarity**: Is the documentation clear and understandable?
- **Consistency**: Does the documentation follow established patterns?
- **Examples**: Does the documentation include helpful examples?

## Documentation Debt

Documentation debt is tracked alongside technical debt:

- **Missing documentation**: Code without documentation
- **Outdated documentation**: Documentation that doesn't match the code
- **Unclear documentation**: Documentation that is hard to understand

## Documentation Metrics

We track the following documentation metrics:

- **Documentation coverage**: Percentage of code with documentation
- **Documentation quality**: Subjective assessment of documentation quality
- **Documentation freshness**: How recently documentation was updated

## Best Practices

1. **Write documentation first**: Consider writing documentation before code
2. **Keep documentation close to code**: Documentation should live as close as possible to the code it describes
3. **Update documentation with code**: Always update documentation when updating code
4. **Use templates**: Use the provided templates for consistency
5. **Include examples**: Examples make documentation more useful
6. **Consider the audience**: Write documentation for the intended audience
7. **Use diagrams**: Visual representations can clarify complex concepts
8. **Link related documentation**: Connect related concepts with links
