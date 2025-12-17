#!/bin/bash

# Script to run the Trips Explorer App on macOS/Linux

# Ensure the script is run from the directory containing it
cd "$(dirname "$0")"

echo "Setting up Trips Explorer App..."

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found in the current directory."
    exit 1
fi

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 could not be found. Please install Python 3."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Error: Could not activate virtual environment."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install pandas streamlit pydeck

# Run the app
echo "Starting Streamlit app..."
streamlit run app.py
