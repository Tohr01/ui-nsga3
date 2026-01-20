#!/bin/bash

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt

  # Post install playwright
  python -m playwright install --with-deps chromium
fi

echo "Virtual environment set up."
