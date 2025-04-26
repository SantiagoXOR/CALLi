# Documentation Integration in CI/CD

This guide explains how documentation is integrated into the CI/CD pipeline for the Call Automation Project.

## Overview

Documentation is treated as a first-class citizen in our development process. The CI/CD pipeline includes steps to validate, build, and deploy documentation alongside code.

## CI/CD Pipeline Steps

### 1. Documentation Validation

The CI pipeline automatically validates documentation:

- **Backend documentation**:
  - Validates RST syntax
  - Checks for broken internal links
  - Validates PlantUML diagrams
  - Ensures docstrings follow Google style

- **Frontend documentation**:
  - Validates Markdown syntax
  - Checks for broken links
  - Ensures JSDoc comments follow project standards

### 2. Documentation Building

If validation passes, the CI pipeline builds the documentation:

- **Backend documentation**:
  - Builds Sphinx documentation
  - Generates HTML output
  - Creates API reference from docstrings

- **Frontend documentation**:
  - No build step required for Markdown files

### 3. Documentation Deployment

On successful builds to the main branch, documentation is automatically deployed:

- **Deployment target**: GitHub Pages
- **URL**: [https://your-organization.github.io/call-automation-project/](https://your-organization.github.io/call-automation-project/)
- **Update frequency**: On every merge to main

## CI/CD Configuration

The documentation CI/CD is configured in `.github/workflows/ci.yml`:

```yaml
# Documentation-related steps in CI workflow
- name: Validate documentation
  run: |
    cd backend-call-automation/docs
    python scripts/validate_diagrams.py
    python scripts/validate_links.py
    make clean
    make diagrams
    make linkcheck
    make html

- name: Generate documentation report
  if: always()
  run: |
    cd backend-call-automation/docs
    echo "# Documentation Status Report" > doc_report.md
    echo "## Validation Results" >> doc_report.md
    echo "* Diagrams: $(test -f _build/diagrams.log && cat _build/diagrams.log || echo 'OK')" >> doc_report.md
    echo "* Links: $(test -f _build/linkcheck/output.txt && cat _build/linkcheck/output.txt || echo 'OK')" >> doc_report.md

- name: Upload documentation report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: documentation-report
    path: backend-call-automation/docs/doc_report.md

- name: Deploy documentation
  if: github.ref == 'refs/heads/main' && success()
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./backend-call-automation/docs/_build/html
```

## Documentation Quality Gates

The CI pipeline enforces the following quality gates for documentation:

1. **No broken links**: All internal and external links must be valid
2. **Valid syntax**: All documentation files must have valid syntax
3. **Complete API docs**: All public APIs must be documented
4. **Valid diagrams**: All PlantUML diagrams must be valid

## Troubleshooting CI/CD Documentation Issues

If the CI pipeline fails due to documentation issues:

1. **Check the documentation report**: Download the documentation report artifact from the GitHub Actions page
2. **Fix validation errors**: Address any syntax, link, or diagram errors
3. **Build locally**: Run the documentation build locally to verify fixes
4. **Update docstrings**: Ensure all code has proper docstrings

## Local Validation

To validate documentation locally before pushing:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit hooks manually
pre-commit run --all-files

# Build backend documentation
cd backend-call-automation/docs
make html
```

## Best Practices

1. **Automate documentation checks**: Use pre-commit hooks to catch documentation issues early
2. **Review documentation changes**: Include documentation review in code reviews
3. **Monitor documentation coverage**: Track documentation coverage over time
4. **Test documentation**: Ensure examples in documentation work as expected
