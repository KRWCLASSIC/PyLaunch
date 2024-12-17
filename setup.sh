#!/bin/bash

# Check if python3 is installed
if command -v python3 &>/dev/null; then
    # Try to run the script with python3
    exec python3 "$(dirname "$0")/main.pyw" "$@"
else
    echo "Python 3 not found! Please install Python 3 or add it to PATH."
    exit 1
fi 