from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import get_bot_response

app = Flask(__name__)
CORS(app, origins=["https://your-site.netlify.app", "http://localhost:3000"])
  # Enable CORS for all routes

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    response = get_bot_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
