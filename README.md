# ai-code-reviewer

AI Code Reviewer is a serverless Python project designed to automatically review code using AI models. It leverages AWS Lambda and Python libraries to analyze code quality, style, and potential issues.

## Features
- Automated code review using AI
- AWS Lambda compatible
- Supports multiple Python libraries
- Easy to deploy as a Lambda function with custom layers

## Project Structure
- `lambda_function.py`: Main Lambda handler and logic
- `layer.zip`, `function.zip`: Deployment packages for AWS Lambda
- `code-reviewer-layer/`, `pythonLambdaLayer/`: Custom Lambda layers with dependencies
- `bin/`, `certifi/`, `charset_normalizer/`, etc.: Included Python packages and binaries

## Setup & Installation
1. Clone the repository:
	```sh
	git clone <repo-url>
	cd ai-code-reviewer
	```
2. (Optional) Create a virtual environment and activate it:
	```sh
	python -m venv venv
	.\venv\Scripts\activate
	```
3. Install dependencies:
	```sh
	pip install -r requirements.txt
	```
	Or manually install required packages as needed.

## Usage
1. Update `lambda_function.py` as needed for your review logic.
2. Package your Lambda function and layers:
	- Zip the contents as required by AWS Lambda.
3. Deploy to AWS Lambda via the AWS Console or CLI.


## License
MIT License. See `LICENSE` file for details.