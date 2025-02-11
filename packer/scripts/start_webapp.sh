#!/bin/bash

LOG_FILE="/opt/webapp/webapp.log"
PID_FILE="/var/run/webapp.pid"

# Ensure old process does not exist (kill if it does)
if [ -f "$PID_FILE" ]; then
    old_pid=$(cat "$PID_FILE")
    if ps -p "$old_pid" > /dev/null; then
        echo "Stopping old process $old_pid"
        kill "$old_pid"
        sleep 2
    fi
fi

# Start Python app and log output
echo "Starting webapp..."
nohup /opt/webapp/venv/bin/python /opt/webapp/run.py > "$LOG_FILE" 2>&1 &

# Record new process PID
echo $! > "$PID_FILE"
echo "Webapp started with PID $(cat $PID_FILE)"