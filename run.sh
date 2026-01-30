#!/bin/bash

# Ensure we are in the directory where the script is located
cd "$(dirname "$0")"

VENV_DIR="venv"

# 1. Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 First-time setup: Creating Python environment..."
    
    # Try to find python3
    if command -v python3 &>/dev/null; then
        PYTHON_CMD=python3
    else
        echo "❌ Error: Python 3 not found. Please install Python."
        exit 1
    fi

    # Create venv
    $PYTHON_CMD -m venv "$VENV_DIR"
    
    # Install dependencies quietly
    echo "⬇️  Installing required libraries (rumps, requests)..."
    ./"$VENV_DIR"/bin/pip install rumps requests --quiet
    
    echo "✅ Setup complete! Starting app..."
fi

# 2. Run the application
./"$VENV_DIR"/bin/python myip_app.py