# Documentation Workflow Guide

This guide outlines the workflow for integrating documentation with the development process in the Call Automation Project.

## Documentation-as-Code Workflow

### 1. Before Writing Code

1. **Understand requirements**: Ensure you understand what you're building and how it fits into the system
2. **Review existing documentation**: Familiarize yourself with related documentation
3. **Plan your changes**: Consider how your changes will be documented

### 2. During Development

1. **Document as you code**:
   - Add docstrings to all new functions, classes, and methods
   - Update existing docstrings when modifying code
   - Use templates from `docs/TEMPLATES/` directory

2. **Write module/component documentation**:
   - Add or update module-level documentation
   - Document architecture decisions in appropriate files

3. **Update related documentation**:
   - Update architecture diagrams if necessary
   - Update user guides if functionality changes

### 3. Before Submitting a PR

1. **Documentation checklist**:
   - [ ] All new code has appropriate docstrings
   - [ ] Modified code has updated docstrings
   - [ ] Module/component documentation is complete
   - [ ] Architecture documentation is updated (if applicable)
   - [ ] User documentation is updated (if applicable)
   - [ ] Documentation builds without errors

2. **Generate and review documentation**:
   - Backend: Run `make html` in `backend-call-automation/docs/`
   - Frontend: Review Markdown files for accuracy

3. **Include documentation changes in PR description**:
   - Mention which documentation was added/updated
   - Explain significant documentation changes

### 4. During Code Review

1. **Review documentation alongside code**:
   - Ensure documentation accurately reflects code behavior
   - Check for clarity and completeness
   - Verify adherence to documentation standards

2. **Address documentation feedback**:
   - Update documentation based on reviewer comments
   - Re-generate documentation if necessary

### 5. After Merging

1. **Verify documentation deployment**:
   - Ensure documentation is correctly built and deployed
   - Check links and references

## Documentation Tools and Commands

### Backend Documentation

```bash
# Navigate to backend docs directory
cd backend-call-automation/docs

# Generate HTML documentation
make html

# Validate documentation
make validate

# Check external links
make linkcheck

# Generate diagrams
make diagrams

# Serve documentation locally
python -m http.server -d _build/html
```

### Frontend Documentation

Frontend documentation is primarily in Markdown files and doesn't require a build step.

## Documentation Location Guide

| Type of Documentation | Location |
|-----------------------|----------|
| Backend API docs | `backend-call-automation/docs/` |
| Frontend component docs | `docs/frontend-components-reference.md` |
| Architecture docs | `docs/architecture/` |
| User guides | `docs/user-guides/` |
| Development guides | `docs/` |
| Code docstrings | Directly in source code |

## Continuous Integration

The CI pipeline automatically:
1. Validates documentation
2. Checks links
3. Builds documentation
4. Deploys documentation to GitHub Pages (on main branch)

## Best Practices

1. **Keep documentation close to code**: Documentation should live as close as possible to the code it describes
2. **Update documentation in the same PR**: Never update code without updating its documentation
3. **Use templates**: Use the provided templates for consistency
4. **Think about the reader**: Write documentation that you would want to read
5. **Use diagrams**: A picture is worth a thousand words
6. **Link related documentation**: Connect related concepts with links
7. **Test your documentation**: Ensure examples work and instructions are accurate
