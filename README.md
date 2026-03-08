# Automated GitHub Pull Request Reviewer

## 1. Project Overview

This project is an event-driven, serverless system that automatically reviews GitHub Pull Requests using Artificial Intelligence.

When a developer opens or updates a Pull Request in GitHub:

1. GitHub sends a webhook event to an AWS API Gateway endpoint.
2. API Gateway triggers an AWS Lambda function.
3. The Lambda function:
   - Extracts Pull Request details
   - Fetches the code diff using the GitHub REST API
   - Sends the code changes to Google Gemini AI for analysis
4. Gemini analyzes the code for:
   - Bugs
   - Code quality issues
   - Security concerns
   - Performance improvements
5. The AI-generated review is posted back as a comment directly on the Pull Request.
6. Execution logs are recorded in AWS CloudWatch.
7. Optional notifications are sent using AWS SNS.

The entire system runs on AWS serverless infrastructure, ensuring scalability, cost efficiency, and minimal operational overhead.

For development and testing purposes, Docker is used locally to simulate the AWS Lambda runtime before deploying to the cloud.

---

## 2. Problem It Solves

Manual code reviews are:
- Time-consuming
- Inconsistent across reviewers
- Dependent on reviewer availability
- A bottleneck in fast-paced development environments

Existing automated tools are often rule-based, expensive, or lack contextual understanding of code changes.

This project solves the problem by:
- Automating Pull Request reviews
- Providing contextual, AI-driven feedback
- Reducing review turnaround time
- Integrating seamlessly into existing GitHub workflows

---

## 3. Target Users (Personas)

### 1. Software Developers
- Create and update Pull Requests frequently
- Want faster feedback on code quality and issues
- Prefer comments directly inside GitHub PRs

### 2. DevOps Engineers / Maintainers
- Manage multiple repositories
- Need scalable and consistent review processes
- Want minimal operational overhead

### 3. Student Developers / Small Teams
- Limited access to senior reviewers
- Benefit from AI-assisted learning and best practices
- Prefer cost-effective, serverless solutions

---

## 4. Vision Statement

> To streamline software development by providing fast, consistent, and intelligent AI-powered Pull Request reviews that enhance code quality while reducing manual effort.

---

## 5. Key Features / Goals

- Automatic detection of GitHub Pull Request events
- Secure webhook handling using AWS API Gateway
- AI-based code analysis using Google Gemini
- Human-like review comments posted directly on PRs
- Serverless, scalable, and cost-efficient architecture
- Real-time notifications using AWS SNS
- Centralized logging and monitoring with CloudWatch

---

## 6. Success Metrics

- AI review comments successfully posted on Pull Requests
- Reduced time between PR creation and review feedback
- Stable system performance under multiple PR events
- Minimal manual intervention after deployment
- Positive developer feedback on usefulness and clarity of reviews

---

## 7. Assumptions & Constraints

### Assumptions
- Users have GitHub repositories with webhook access
- Pull Requests contain meaningful code diffs
- API credentials are configured securely
- Developers are willing to use AI-generated feedback

### Constraints
- Dependent on GitHub and Gemini API availability
- Limited by API rate limits and response latency
- Runs entirely on serverless infrastructure
- Review quality depends on AI model responses

---

## 8. Docker Usage (Local Development & Testing)

### Purpose of Using Docker

This project uses **Docker only for local development and testing**, not for production deployment.

Since the application is built on **AWS Lambda (serverless)**, Docker is used to:
- Simulate the AWS Lambda runtime locally
- Test the Lambda function offline before deploying to AWS
- Ensure environment consistency between local development and production
- Validate webhook handling logic using mock GitHub Pull Request payloads

The production system continues to run fully on **AWS Serverless infrastructure**.

---

### Docker Setup Overview

Docker runs the Lambda function inside an official AWS Lambda base image.  
The container exposes the Lambda Runtime API on a local port, allowing the function to be invoked via HTTP requests.

**Key points:**
- No UI or web server is exposed
- Docker does not replace AWS Lambda
- Docker is not used in production

---

### Files Used for Docker

- `Dockerfile` – Defines the Lambda runtime environment  
- `app.py` – Contains the Lambda handler logic  
- `requirements.txt` – Python dependencies  
- `.env` – Stores environment variables for local testing (not committed)

---

### Environment Variables

Sensitive credentials are not hardcoded.

For local testing, environment variables are loaded from a `.env` file:

```env
GITHUB_PAT=your_github_token
GEMINI_API_KEY=your_gemini_api_key
LOCAL_DOCKER=true
```

## 9. Branching Strategy

This repository follows a lightweight branching strategy tailored to the development of a serverless, AI-powered Pull Request review system.

### Branch Structure

**1. main**

- Represents the stable and production-ready version of the project.
- Contains the deployed AWS serverless implementation.
- Includes the `project/` directory, which contains Docker-based local development support.
- Only validated and tested code is maintained here.

**2. local-dev**

- Used for local experimentation and development.
- Primarily focused on Docker-based Lambda simulation and local testing.
- Allows safe testing of environment variable configurations, webhook parsing, and AI logic without affecting the stable `main` branch.
- Changes from `local-dev` are merged into `main` once verified.

---

### Development Workflow

1. New features or experiments are developed in `local-dev`.
2. Docker is used for local Lambda runtime simulation.
3. Once functionality is verified, changes are merged into `main`.
4. The `main` branch reflects the stable, production-aligned state of the system.

---

### Rationale

This strategy provides:
- Separation between stable and experimental code
- Safe local Docker testing
- Reduced risk of breaking production-ready logic
- Clear organization between cloud deployment and local development

---

## Software Design

### Architecture Diagram
![System Architecture](./design/arch%20diag/archDiag.drawio.png)

![System Architecture](./design/arch%20diag/image.png)


The system uses an **event-driven serverless architecture** where GitHub Pull Request events trigger processing through **AWS API Gateway and AWS Lambda**. The Lambda function retrieves code changes via the **GitHub REST API**, sends them to **Google Gemini AI** for analysis, and posts the review back to the PR. **AWS CloudWatch, SNS, and Secrets Manager** handle logging, notifications, and secure credential management.

---
