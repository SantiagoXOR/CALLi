#!/usr/bin/env node
/**
 * Script to check TypeScript/JavaScript files for JSDoc compliance.
 *
 * This script validates that TypeScript/JavaScript files have proper JSDoc
 * comments for functions, classes, interfaces, and components.
 */

const fs = require('fs');
const path = require('path');
const ts = require('typescript');

/**
 * Check if a node has a JSDoc comment
 *
 * @param {ts.Node} node - TypeScript AST node
 * @param {string} sourceFile - Source file text
 * @returns {boolean} True if node has JSDoc
 */
function hasJSDoc(node, sourceFile) {
  const nodePos = node.getFullStart();
  const nodeText = sourceFile.substring(0, nodePos).trim();

  // Check for JSDoc comment (/**...*/)
  return nodeText.endsWith('*/') && nodeText.includes('/**');
}

/**
 * Check JSDoc for a specific file
 *
 * @param {string} filePath - Path to the file to check
 * @returns {string[]} Array of error messages
 */
function checkFile(filePath) {
  const errors = [];
  const sourceFile = fs.readFileSync(filePath, 'utf8');

  // Parse the file
  const tsSourceFile = ts.createSourceFile(
    filePath,
    sourceFile,
    ts.ScriptTarget.Latest,
    true
  );

  // Visit each node
  function visit(node) {
    // Check for exported declarations that should have JSDoc
    if (
      (ts.isClassDeclaration(node) ||
       ts.isFunctionDeclaration(node) ||
       ts.isInterfaceDeclaration(node) ||
       ts.isTypeAliasDeclaration(node)) &&
      hasModifier(node, ts.SyntaxKind.ExportKeyword)
    ) {
      if (!hasJSDoc(node, sourceFile)) {
        const name = node.name ? node.name.text : 'anonymous';
        const type = getNodeType(node);
        errors.push(`Missing JSDoc for exported ${type} '${name}' in ${filePath}`);
      }
    }

    // Check React components (functions that return JSX)
    if (ts.isFunctionDeclaration(node) || ts.isArrowFunction(node)) {
      const name = node.name ? node.name.text : 'anonymous';
      if (isReactComponent(node) && !hasJSDoc(node, sourceFile)) {
        errors.push(`Missing JSDoc for React component '${name}' in ${filePath}`);
      }
    }

    // Continue traversing
    ts.forEachChild(node, visit);
  }

  // Start traversal
  visit(tsSourceFile);

  return errors;
}

/**
 * Check if a node has a specific modifier
 *
 * @param {ts.Node} node - TypeScript AST node
 * @param {ts.SyntaxKind} kind - Modifier kind to check for
 * @returns {boolean} True if node has the modifier
 */
function hasModifier(node, kind) {
  return node.modifiers &&
         node.modifiers.some(modifier => modifier.kind === kind);
}

/**
 * Get a human-readable type for a node
 *
 * @param {ts.Node} node - TypeScript AST node
 * @returns {string} Human-readable type
 */
function getNodeType(node) {
  if (ts.isClassDeclaration(node)) return 'class';
  if (ts.isFunctionDeclaration(node)) return 'function';
  if (ts.isInterfaceDeclaration(node)) return 'interface';
  if (ts.isTypeAliasDeclaration(node)) return 'type';
  return 'declaration';
}

/**
 * Check if a function is likely a React component
 *
 * @param {ts.Node} node - TypeScript AST node
 * @returns {boolean} True if node appears to be a React component
 */
function isReactComponent(node) {
  // This is a simplified check - in a real implementation,
  // you would do more thorough analysis of the return type
  const name = node.name ? node.name.text : '';
  return name.match(/[A-Z][a-zA-Z]*/) !== null; // Component names are PascalCase
}

/**
 * Main function
 */
function main() {
  const files = process.argv.slice(2);

  if (files.length === 0) {
    console.log('No files to check');
    process.exit(0);
  }

  let hasErrors = false;

  files.forEach(file => {
    if (file.endsWith('.ts') || file.endsWith('.tsx') ||
        file.endsWith('.js') || file.endsWith('.jsx')) {
      const errors = checkFile(file);

      if (errors.length > 0) {
        hasErrors = true;
        errors.forEach(error => console.log(error));
      }
    }
  });

  process.exit(hasErrors ? 1 : 0);
}

// Run the script
main();
