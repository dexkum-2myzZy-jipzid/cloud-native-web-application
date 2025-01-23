**Name** : Liang Chen

**EC2 Instance Type**: t2.micro

**OS**: Ubuntu 20.04 LTS

**Language**: Python 3.12.3

**Web Server Framework Used**: Flask

**Build and Deploy Instructions**:

1. **Trigger Conditions**:
   - On pull request to `main` branch.
2. **Deployment Job**:
   - **Runs on**: `ubuntu-latest`
   - **Environment**: `AWS_DEPLOYMENT`
3. **Steps**:
   1. Checkout code.
   2. Configure AWS credentials.
   3. Check EC2 instance status.
   4. Start EC2 instance if stopped.
   5. Wait for EC2 instance to be running.
   6. Get EC2 instance public IP.
   7. Deploy Flask App to EC2:
      - Create SSH key file.
      - Stop running app if it exists.
      - Remove existing app directory.
      - Create new deployment directory.
      - Install necessary packages.
      - Create and activate virtual environment.
      - Copy all files from root to EC2.
      - Install dependencies from requirements.txt on EC2.
      - Start Flask app.
   8. Setup Variables for Grader Workflow.
   9. Upload Grader Environment Variables.
