#!/bin/bash
set -e

# Set environment variables
export DEBIAN_FRONTEND=noninteractive
export CHECKPOINT_DISABLE=1
export TZ=America/Los_Angeles

echo "Updating system and installing required packages..."
sudo apt-get clean
sudo apt-get update
sudo apt-get upgrade -y

# Install required dependencies
# sudo apt-get install -y --fix-missing unzip python3 python3-pip python3-venv yq nginx
sudo apt-get install -y --fix-missing unzip python3 python3-pip python3-venv yq

# Clean up package cache
sudo apt-get clean -y