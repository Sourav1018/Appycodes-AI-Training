#!/bin/bash


# Fail fast if something goes wrong
set -e

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

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
