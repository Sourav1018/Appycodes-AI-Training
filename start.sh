#!/bin/bash

set -eu  # Exit on error & undefined variables

echo "🔍 Checking virtual environment..."

# Detect Python command (python3 preferred, fallback to python)
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "❌ Python is not installed or not found in PATH!"
    exit 1
fi

# Create virtual environment if not found
if [ ! -d "venv" ]; then
    echo "❗️Virtual environment not found. Creating one with $PYTHON..."
    $PYTHON -m venv venv
    echo "✅ Virtual environment created."
fi

# Step 2: Activate the virtual environment (cross-platform)
echo "⚙️ Activating virtual environment..."
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Failed to activate virtual environment!"
    exit 1
fi
# Install dependencies (if requirements.txt exists)
if [ -f "requirements.txt" ]; then
    echo "Installing required Python packages..."
    pip install -r requirements.txt
fi

echo "Starting FastAPI App..."

# Export environment variables from .env (if exists)
if [ -f ".env" ]; then
    echo "Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

# Set reload flag if RELOAD=true
RELOAD_FLAG=""
if [ "$RELOAD" = "true" ]; then
    echo "Reload mode enabled"
    RELOAD_FLAG="--reload"
fi

# Run uvicorn with logging and production settings
uvicorn app.main:app \
    --host ${HOST:-localhost} \
    --port ${PORT:-8000} \
    --workers 4 \
    --log-level debug \
    $RELOAD_FLAG
