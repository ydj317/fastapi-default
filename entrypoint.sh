#!/bin/bash
set -e

echo "📦 Running 'uv sync'..."
/root/.local/bin/uv sync

echo "🚀 Starting server with uvicorn..."
exec .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
