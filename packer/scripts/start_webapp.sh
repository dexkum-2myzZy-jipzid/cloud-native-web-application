#!/bin/bash

LOG_FILE="/opt/webapp/webapp.log"


# Start Python app and log output
echo "Starting webapp..."
nohup /opt/webapp/venv/bin/python /opt/webapp/run.py > "$LOG_FILE" 2>&1 &