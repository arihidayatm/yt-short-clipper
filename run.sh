#!/bin/bash

# Clean script to run YT Short Clipper with proper environment

# Kill any existing processes
pkill -f "python.*app.py" 2>/dev/null || true

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Run the app with the virtual environment
echo "Starting YT Short Clipper..."
./venv/bin/python app.py "$@"
