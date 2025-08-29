import os
import json
import requests
import time

def lambda_handler(event, context):
    # Extract parameters
    repo_name = event.get("repo", "default-repo")
    file_content = event.get("file_content", "")
    file_name = event.get("file_name", "unknown_file")
    language = event.get("language", "")
    
    gemini_api_key = os.environ["GEMINI_API_KEY"]
    
    # System-style prompt for Gemini
    system_prompt = """You are an expert code reviewer. Provide a thorough code review including:
    1. Code quality assessment
    2. Potential bugs or issues
    3. Security vulnerabilities
    4. Performance optimizations
    5. Best practices recommendations
    6. Readability and maintainability suggestions
    
    Be constructive and provide specific examples for improvements."""
    
    # User request
    user_message = f"""Please review this code from {repo_name}:
    
    File: {file_name}
    Language: {language if language else 'Not specified'}
    
    Code:
    {file_content}
    
    Provide a comprehensive code review."""
    
    # Gemini request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt},
                    {"text": user_message}
                ]
            }
        ]
    }
    
    try:
        start_time = time.time()
        
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {gemini_api_key}"
            },
            json=payload,
            timeout=45
        )
        response.raise_for_status()
        
        result = response.json()
        
        # Extract the text response correctly
        review = result["candidates"][0]["content"]["parts"][0]["text"]
        processing_time = time.time() - start_time
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "repo": repo_name,
                "file_name": file_name,
                "language": language,
                "review": review,
                "processing_time": round(processing_time, 2),
                "model_used": "gemini-1.5-flash"
            }, ensure_ascii=False)
        }
        
    except requests.exceptions.Timeout:
        return {
            "statusCode": 408,
            "body": json.dumps({"error": "Request timeout - Gemini API took too long to respond"})
        }
    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Gemini API request failed: {str(e)}"})
        }
    except (KeyError, IndexError) as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Unexpected response format from Gemini API: {str(e)}"})
        }
