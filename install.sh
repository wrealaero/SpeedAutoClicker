#!/bin/bash

echo "Installing SpeedAutoClicker dependencies..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing pip3..."
    python3 -m ensurepip
fi

# Install required packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt

echo "Installation complete! Run the auto clicker with: python3 SpeedAutoClicker/main.py"