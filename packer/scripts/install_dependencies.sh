#!/bin/bash
set -e

echo "Cleaning up and updating system packages..."
sudo apt-get clean
sudo apt-get update
sudo apt-get upgrade -y

echo "Installing required dependencies..."
sudo apt-get install -y --fix-missing unzip python3 python3-pip python3-venv yq