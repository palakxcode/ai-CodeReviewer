def run_review(repo_full, pr_number, diff_content):
    #---step-7----
    if not diff_content:
        msg = "No diff content found — skipping Gemini review."
        print(msg)
        return {"statusCode": 200, "body": msg}

    # --- Step 5: Build prompt for Gemini ---
    user_message = f"""
You are an expert software reviewer.
Review this GitHub Pull Request diff from repository '{repo_full}'.

Provide a thorough review including:
- Summary of changes
- Possible bugs or issues
- Code quality and maintainability
- Security or performance issues
- Suggested improvements

Here is the diff:
{diff_content}
"""

    # --- Step 6: Call Gemini API ---
    start_time = time.time()
    try:
        gemini_url = (
            f"https://generativelanguage.googleapis.com/v1/models/"
            f"gemini-2.5-flash:generateContent?key={gemini_api_key}"
        )
        resp = requests.post(
            gemini_url,
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": user_message}]}]},
            timeout=45
        )
        print("Gemini status:", resp.status_code)
        resp.raise_for_status()
        review = (
            resp.json()
            .get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "No review.")
        )
    except Exception as e:
        print("Gemini error:", repr(e))
        review = "Gemini API call failed."

    duration = time.time() - start_time
    print(f"AI processing time: {duration:.2f}s")

    # --- Step 7: Post review to GitHub ---
    comment_posted = False
    if github_token and repo_full and pr_number:
        try:
            comment_url = f"https://api.github.com/repos/{repo_full}/issues/{pr_number}/comments"
            comment_headers = {
                "Authorization": f"Bearer {github_token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "ai-code-review-lambda"
            }
            comment_body = {
                "body": f"🤖 **Gemini Code Review**\n\n{review}\n\n_Time taken: {duration:.2f}s_"
            }
            post_resp = requests.post(comment_url, headers=comment_headers, json=comment_body, timeout=20)
            print("Comment response:", post_resp.status_code)
            if post_resp.status_code == 201:
                comment_posted = True
        except Exception as e:
            print("GitHub comment error:", repr(e))
    else:
        print("Skipping comment post (missing details)")

    return review
