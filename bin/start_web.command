#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to that directory
cd "$DIR"

# Print banner
echo "=========================================="
echo "  Hash Cracker - Web Interface"
echo "=========================================="
echo ""
echo "Starting web server..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3 first."
    read -p "Press Enter to exit..."
    exit 1
fi

# Kill any existing server on port 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null

# Start the web server
python3 web_server.py

# Keep terminal open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo "Server stopped with error"
    read -p "Press Enter to exit..."
fi
