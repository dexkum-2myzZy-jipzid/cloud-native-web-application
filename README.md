# Cloud Native Web Application

## Overview

This project is a cloud-native web application built with Python and Flask, focusing on automated deployment, scalability, and high availability. It leverages modern DevOps practices such as automated image building, CI/CD with GitHub Actions, cloud monitoring, and serverless API deployment.

## Key Features

- **RESTful API**: Endpoints for movie info, ratings, links, and health checks.
- **User Authentication**: JWT-based registration and login for secure access.
- **Automated Deployment**: CI/CD pipeline with GitHub Actions for seamless deployment and environment setup.
- **Custom AMI**: Automated dependency installation and configuration using Packer.
- **Cloud Monitoring**: CloudWatch Agent auto-installation and configuration for system and app metrics.
- **Database Automation**: MySQL instance provisioning and EBS volume setup.
- **Serverless Support**: AWS Lambda implementation for API endpoints.
- **Auto-Grading**: Integrated grader scripts for assignment evaluation.

## Project Structure

- `app/`: Core Flask application (routes, middleware, config)
- `database/`: Database connection pooling and operations
- `scripts/`: Data processing and maintenance scripts
- `packer/`: Packer build scripts and configs
- `grader/`: Auto-grading tools
- `assignment12/`: Lambda-related code and configs

## Deployment

See the Build and Deploy Instructions section in this README for one-click automated deployment to AWS.

---

For detailed API docs, deployment steps, or more info, check the subfolders or source code comments.
