# Vasantha_Challenge

## Overview

This repository contains the code for deploying a scalable and secure static web application on AWS. It includes:
- CloudFormation template for setting up the EC2 instance and security group.
- Ansible playbook for configuring the web server and SSL.
- Automated test script to verify the deployment.

## Setup

1. **Deploy CloudFormation Stack**
   - Navigate to AWS CloudFormation.
   - Create a new stack using `cloudformation-template.yml`.

2. **Configure Web Server**
   - SSH into the EC2 instance.
   - Run the Ansible playbook: `ansible-playbook -i <your-instance-ip>, playbook.yml`.

3. **Run Automated Tests**
   - Run the test script: `bash test_deployment.sh`.

## Requirements

- AWS Account
- Ansible installed locally
- Key pair for EC2 access

## License

