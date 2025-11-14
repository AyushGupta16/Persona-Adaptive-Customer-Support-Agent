import json
from local_llm import chat

def detect_persona(user_message: str) -> dict:
    prompt = f"""
Classify the user's persona into exactly one of:
1. Technical Expert
2. Frustrated User
3. Business Executive

User message: {user_message}

Respond ONLY in JSON exactly like:
{{"persona": "<one of three>", "reason": "short explanation"}}
"""

    messages = [
        {
            "role": "system",
            "content": "You are a strict JSON classifier. Return only valid JSON."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    content = chat(messages)

    try:
        return json.loads(content)
    except Exception:
        # Return default on parse error
        return {"persona": "Business Executive", "reason": "fallback - malformed LLM output"}
