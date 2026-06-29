#!/bin/bash

set -e 

# Check if user has uv in their PATH
if ! command -v uv &> /dev/null
then
    echo "uv could not be found. Please install uv and add it to your PATH."
    exit 2
fi

uv sync
uv run playwright install

echo "Setup complete."
