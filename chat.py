import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import get_bot_response

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    response = get_bot_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    # Fetch the port from the environment variable (e.g., for deployment)
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not set
    app.run(host="0.0.0.0", port=port)  # Allow external access for deployment
