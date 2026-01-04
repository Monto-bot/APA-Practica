#!/bin/bash

VENV_DIR=".venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install requirements if they exist
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

echo "Virtual environment activated"
# Read user input
read -p "Enter command (update/exit): " command

if [ "$command" = "update" ]; then
    echo "Updating requirements..."
    pip install -r requirements.txt
elif [ "$command" = "exit" ]; then
    echo "Exiting..."
    exit 0
else
    echo "Unknown command: $command"
fi
# Keep the shell interactive after script execution
exec bash