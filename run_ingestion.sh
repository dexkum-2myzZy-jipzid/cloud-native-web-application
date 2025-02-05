#!/bin/bash

# Print message indicating the activation of the virtual environment
echo "Activating virtual environment..."

# Activate the virtual environment
source venv/bin/activate

# Print message indicating the running of the ingestion script
echo "Running ingestion script..."

# Run the ingestion script
python movies_ingest.py