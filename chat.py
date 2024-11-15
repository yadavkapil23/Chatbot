from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated chatbot logic (replace this with your chatbot code)
def chatbot_response(user_input):
    return f"You said: {user_input}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
