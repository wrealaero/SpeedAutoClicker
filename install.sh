#!/bin/bash

echo "Installing SpeedAutoClicker dependencies..."

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install Python 3 and pip3 
first."
    exit 1
fi

# Install required packages
pip3 install -r requirements.txt

echo "Installation complete! Run the application with: python3 
SpeedAutoClicker/main.py"

