#!/bin/bash
# Development server script for Gateway API

set -e

# Default values
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
RELOAD="${RELOAD:-true}"

echo "Starting Gateway API..."
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Reload: $RELOAD"

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv..."
    if [ "$RELOAD" = "true" ]; then
        uv run uvicorn gateway.main:app --host "$HOST" --port "$PORT" --reload
    else
        uv run uvicorn gateway.main:app --host "$HOST" --port "$PORT"
    fi
else
    echo "Using python..."
    if [ "$RELOAD" = "true" ]; then
        python -m uvicorn gateway.main:app --host "$HOST" --port "$PORT" --reload
    else
        python -m uvicorn gateway.main:app --host "$HOST" --port "$PORT"
    fi
fi
