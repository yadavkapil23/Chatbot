from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
api_key = os.getenv("api_key")

# API configuration
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Function to strip markdown characters
def strip_markdown(text):
    return re.sub(r'[*_`~]', '', text)

# Function to format text as a code block
def format_code_blocks(text):
    # Add triple backticks around code blocks
    return re.sub(r'```(.*?)```', r'```\1```', text, flags=re.DOTALL)

# Function to get the bot's response
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

# Flask app configuration
app = Flask(__name__)
CORS(app)  


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')  # Extract user message
    print(f"Received user input: {user_input}")  # Debug log
    
    # Get bot response
    bot_response = get_bot_response(user_input)
    
    # Remove markdown characters from the response
    clean_response = strip_markdown(bot_response)
    
    # Format the response with code blocks
    formatted_response = format_code_blocks(clean_response)
    
    return jsonify({"response": formatted_response})

if __name__ == '__main__':
    app.run(debug=True)
