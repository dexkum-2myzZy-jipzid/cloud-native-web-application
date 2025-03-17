#!/bin/bash

set -e

echo "Downloading Amazon CloudWatch Agent..."
sudo wget -q https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb -O /tmp/amazon-cloudwatch-agent.deb

echo "Installing Amazon CloudWatch Agent..."
sudo dpkg -i -E /tmp/amazon-cloudwatch-agent.deb

rm /tmp/amazon-cloudwatch-agent.deb

sudo mkdir -p /opt/aws/amazon-cloudwatch-agent/etc

echo "Moving CloudWatch Agent configuration..."
sudo mv /tmp/amazon-cloudwatch-agent.json /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json

echo "Starting Amazon CloudWatch Agent..."
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
    -s

echo "Enabling CloudWatch Agent to start on boot..."
sudo systemctl enable amazon-cloudwatch-agent

echo "CloudWatch Agent setup completed!"