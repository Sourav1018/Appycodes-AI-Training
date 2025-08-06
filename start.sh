#!/bin/bash

# Fail fast if something goes wrong
set -e

echo "Starting FastAPI App..."

# Export env variables
export $(grep -v '^#' .env | xargs)

# Run uvicorn with logging and production settings
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --workers 4 \
    --log-level debug
