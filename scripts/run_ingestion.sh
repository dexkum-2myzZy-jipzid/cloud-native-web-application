#!/bin/bash

# Print virtual environment activation message
echo "Activating virtual environment..."

# Activate virtual environment (assuming venv is in the project root)
source venv/bin/activate

# Print script execution message
echo "Running ingestion script..."

# Run data ingestion script (adjust path)
python scripts/movies_ingest.py  # Key modification point

# Optional: deactivate virtual environment after execution (add if needed)
# deactivate