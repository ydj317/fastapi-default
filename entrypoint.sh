#!/bin/bash
set -e

echo "📦 Running 'uv sync'..."
uv sync

echo "🚀 Starting server..."
exec "$@"
