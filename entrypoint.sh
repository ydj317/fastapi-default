#!/bin/bash
set -e

echo "📦 Running 'uv sync'..."
#uv sync

echo "🚀 Starting server with uvicorn..."
#exec .venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
exec "bash"