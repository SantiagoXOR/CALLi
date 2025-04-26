# Documentation Update Checklist

Use this checklist when making changes to the codebase to ensure documentation is properly updated.

## Code Changes

### Backend (Python)

- [ ] Added docstrings to all new functions, classes, and methods
- [ ] Updated existing docstrings for modified code
- [ ] Docstrings follow Google style format
- [ ] Module-level docstrings explain the purpose of the module
- [ ] Type hints are used consistently
- [ ] Examples are provided for complex functionality
- [ ] Edge cases and exceptions are documented

### Frontend (TypeScript/React)

- [ ] Added JSDoc comments to all new functions, components, and types
- [ ] Updated existing JSDoc comments for modified code
- [ ] Component props are documented
- [ ] Component examples are provided
- [ ] Hook usage is documented
- [ ] Edge cases are documented

## Architecture Documentation

- [ ] Updated architecture diagrams if the architecture changed
- [ ] Updated service documentation if service interfaces changed
- [ ] Updated data flow diagrams if data flow changed
- [ ] Updated integration documentation if integration points changed

## API Documentation

- [ ] Updated API endpoint documentation for new/modified endpoints
- [ ] Updated request/response examples
- [ ] Updated error documentation
- [ ] Updated authentication/authorization requirements

## User Documentation

- [ ] Updated user guides for new/modified features
- [ ] Updated screenshots for UI changes
- [ ] Updated workflow descriptions for process changes
- [ ] Updated troubleshooting sections for known issues

## General Documentation

- [ ] Documentation builds without errors
- [ ] Links are valid
- [ ] Spelling and grammar are correct
- [ ] Formatting is consistent
- [ ] Documentation is clear and understandable

## Pre-Commit Checks

- [ ] Run pre-commit hooks to validate documentation
- [ ] Fix any issues reported by pre-commit hooks
- [ ] Build documentation locally to verify changes

## Pull Request

- [ ] Include documentation changes in the PR description
- [ ] Link to relevant documentation files in the PR
- [ ] Request documentation review if changes are significant

## Post-Merge

- [ ] Verify documentation is correctly built and deployed
- [ ] Check links and references in the deployed documentation
- [ ] Address any issues found in the deployed documentation
