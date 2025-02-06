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
6. Get stack outputs and extract public IPs, private IPs, and Database Instance ID.
7. Attach EBS Volume to the Database EC2 instance.
8. Configure EBS Volume (mount, set permissions, restart MySQL service).
9. Setup environment on WebApp EC2.
10. Create and copy `.env` file to EC2 with database instance IP.
11. Launch Flask app on EC2 using `nohup`.
12. Setup grader workflow variables and upload them as an artifact.
