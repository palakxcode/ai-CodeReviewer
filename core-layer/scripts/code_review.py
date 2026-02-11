import os
import json
import requests

# Get repo info from GitHub environment variables
repo_name = os.environ.get("GITHUB_REPOSITORY")
pr_number = os.environ.get("GITHUB_REF")  # Pull request branch
file_name = "example.py"

# Read file content (example: check out file in the repo)
with open(file_name, "r") as f:
    file_content = f.read()

user_message = f"""Please review this code from {repo_name} (PR {pr_number}):

File: {file_name}

Code:
{file_content}

Provide a comprehensive code review.
"""

response = requests.post(
    "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent",
    headers={"Authorization": f"Bearer {os.environ['GEMINI_API_KEY']}"},
    json={"contents": [{"text": user_message}]}
)
review = response.json()
print(json.dumps(review, indent=2))
