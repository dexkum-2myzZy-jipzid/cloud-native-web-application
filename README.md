# Project Deployment Guide

**Name**: Liang Chen

**EC2 Instance Type**: t2.micro

**OS**: Ubuntu 20.04 LTS

**Language**: Python 3.12.3

**Web Server Framework Used**: Flask

## Build and Deploy Instructions

### Trigger Conditions

- **On push** to the `feature/*` or `main` branches.
- **On pull request** to the `main` branch.

### Deployment Job

- **Runs on**: `ubuntu-latest`
- **Environment**: `AWS_DEPLOYMENT`

### Steps

1. Checkout code.
2. Configure AWS credentials.
3. Delete existing CloudFormation stack if it exists.
4. Create VPC and subnets using the `vpc.yaml` template.
5. Wait for stack creation to complete.
6. Get stack outputs and extract public and private IPs.
7. Setup environment on EC2: create SSH key, copy files, and install packages.
8. Create and copy `.env` file to EC2.
9. Ingest movies data using `movies_ingest.py`.
10. Launch Flask app on EC2.
11. Setup grader workflow variables.
12. Upload grader environment variables.
