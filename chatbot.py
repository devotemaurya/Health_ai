import os
import requests

def ask_together_ai(prompt):
    api_key = os.getenv("TOGETHER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a helpful health assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        output = response.json()
        reply = output["choices"][0]["message"]["content"].strip()
        return reply
    except Exception as e:
        print("Chatbot error:", e)
        return "Sorry, I'm having trouble reaching the chatbot."
