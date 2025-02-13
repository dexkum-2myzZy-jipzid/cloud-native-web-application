#!/bin/bash
set -e

# Create group csye6225 (if not exists)
sudo groupadd -f csye6225

# Create user csye6225 (if not exists)
if ! id "csye6225" &>/dev/null; then
    sudo useradd -r -g csye6225 -s /usr/sbin/nologin csye6225
fi

# Create WebApp directory and set permissions
sudo mkdir -p /opt/webapp
sudo chown -R csye6225:csye6225 /opt/webapp