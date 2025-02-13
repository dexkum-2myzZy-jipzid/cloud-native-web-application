#!/bin/bash
set -e

# Extract WebApp code to /opt/webapp
echo "Extracting webapp..."
mkdir -p /opt/webapp
unzip /tmp/webapp.zip -d /opt/webapp
sudo cp /tmp/start_webapp.sh /opt/webapp/start_webapp.sh
sudo chmod +x /opt/webapp/start_webapp.sh

# Copy systemd service file
echo "Setting up systemd service..."
sudo cp /tmp/webapp.service /etc/systemd/system/webapp.service
sudo systemctl daemon-reload
sudo systemctl enable webapp.service

# Set directory ownership
echo "Setting ownership for /opt/webapp..."
sudo chown -R csye6225:csye6225 /opt/webapp

# Create Python virtual environment and install dependencies
echo "Setting up Python environment..."
sudo -u csye6225 python3 -m venv /opt/webapp/venv
sudo -u csye6225 /opt/webapp/venv/bin/pip install --upgrade pip
sudo -u csye6225 /opt/webapp/venv/bin/pip install -r /opt/webapp/requirements.txt