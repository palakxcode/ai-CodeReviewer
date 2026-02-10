# app.py

import os
import json
import requests
import time

GITHUB_TOKEN = os.getenv("GITHUB_PAT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def lambda_handler(event, context):
    """
    Docker + Lambda compatible version of
    AI-Powered GitHub Pull Request Reviewer
    """

    # --- Basic safety ---
    body = event.get("body", {})
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            body = {}

    # --- Check PR event ---
    if "pull_request" not in body:
        return {
            "statusCode": 200,
            "body": "Not a pull request event"
        }

    pr = body["pull_request"]
    repo = body["repository"]["full_name"]
    pr_number = pr["number"]

    # --- Environment variables (same as AWS) ---
    GITHUB_TOKEN = os.getenv("GITHUB_PAT", "dummy")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "dummy")

    # --- Fetch PR diff ---
    diff_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }

    diff_response = requests.get(diff_url, headers=headers)
    diff_content = diff_response.text if diff_response.status_code == 200 else ""

    if not diff_content:
        return {
            "statusCode": 200,
            "body": "No diff found"
        }

    # --- Build Gemini prompt ---
    prompt = f"""
    You are an expert code reviewer.
    Review the following GitHub Pull Request diff:

    {diff_content}
    """

    # --- Call Gemini (mock-safe for Docker) ---
    start = time.time()
    review_text = "Gemini review simulated (Docker test mode)"
    duration = round(time.time() - start, 2)

    # --- Return response (Docker visible) ---
    return {
        "statusCode": 200,
        "body": json.dumps({
            "repository": repo,
            "pr_number": pr_number,
            "review": review_text,
            "time_taken": duration
        })
    }