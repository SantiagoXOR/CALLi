#!/bin/bash
# Script to check if documentation is updated with code changes

# Get list of changed files
CHANGED_FILES=$(git diff --cached --name-only)

# Initialize error flag
HAS_ERRORS=0

# Function to check if a Python file has been modified
check_python_file() {
    local file=$1
    
    # Check if the file exists and is a Python file
    if [[ -f "$file" && "$file" == *.py ]]; then
        # Extract module name from file path
        MODULE_NAME=$(basename "$file" .py)
        MODULE_PATH=$(dirname "$file" | sed 's/\//./g')
        FULL_MODULE="$MODULE_PATH.$MODULE_NAME"
        
        # Look for documentation references to this module
        DOC_FILES=$(grep -r --include="*.rst" --include="*.md" "$MODULE_NAME" backend-call-automation/docs/ docs/ 2>/dev/null || true)
        
        if [[ -z "$DOC_FILES" ]]; then
            echo "Warning: No documentation found for modified Python module: $FULL_MODULE"
            # Don't fail the commit for this, just warn
        fi
    fi
}

# Function to check if a TypeScript/JavaScript file has been modified
check_ts_file() {
    local file=$1
    
    # Check if the file exists and is a TypeScript/JavaScript file
    if [[ -f "$file" && ("$file" == *.ts || "$file" == *.tsx || "$file" == *.js || "$file" == *.jsx) ]]; then
        # Extract component name from file path
        COMPONENT_NAME=$(basename "$file" | sed 's/\.[^.]*$//')
        
        # Look for documentation references to this component
        DOC_FILES=$(grep -r --include="*.md" "$COMPONENT_NAME" docs/ 2>/dev/null || true)
        
        if [[ -z "$DOC_FILES" ]]; then
            echo "Warning: No documentation found for modified component: $COMPONENT_NAME"
            # Don't fail the commit for this, just warn
        fi
    fi
}

# Check each changed file
for file in $CHANGED_FILES; do
    # Skip documentation files themselves
    if [[ "$file" == docs/* || "$file" == backend-call-automation/docs/* ]]; then
        continue
    fi
    
    # Check Python files
    if [[ "$file" == *.py ]]; then
        check_python_file "$file"
    fi
    
    # Check TypeScript/JavaScript files
    if [[ "$file" == *.ts || "$file" == *.tsx || "$file" == *.js || "$file" == *.jsx ]]; then
        check_ts_file "$file"
    fi
done

# Exit with error code if there were errors
exit $HAS_ERRORS
