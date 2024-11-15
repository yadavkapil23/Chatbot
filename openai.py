import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("api_key")


url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_bot_response(user_input):
    data = {
        "model": "gemma2-9b-it",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        bot_reply = response.json()["choices"][0]["message"]["content"]
        return bot_reply
    else:
        return f"Error: {response.status_code}, {response.text}"
