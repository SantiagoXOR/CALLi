#!/bin/bash

# Validación Backend
echo "🔍 Validando backend..."
cd backend-call-automation

echo "Running Ruff..."
ruff check .

echo "Running MyPy..."
mypy .

echo "Running Tests..."
pytest

# Validación Frontend
echo "🔍 Validando frontend..."
cd ../frontend-call-automation

echo "Running ESLint..."
npm run lint

echo "Running TypeScript Check..."
npm run type-check

echo "Running Tests..."
npm run test

echo "✅ Validación completada"
