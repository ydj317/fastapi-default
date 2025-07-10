#!/bin/bash
set -e

cd /app

echo "📦 Running 'uv sync'..."
/root/.local/bin/uv sync

echo "🚀 Starting server with uvicorn..."
exec .venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
