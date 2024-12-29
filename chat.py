import threading
import datetime
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import re
import mysql.connector

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

# MySQL Database Connection Class
class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establishes a database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "Neobot"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "1234")
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")

    def disconnect(self):
        """Closes the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """Executes a query with optional parameters."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query, params=None):
        """Fetches all results from a query."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def add_message(self, user_id, message):
        """Adds a message to the database."""
        query = "INSERT INTO chats (user_id, message, timestamp) VALUES (%s, %s, %s)"
        self.execute_query(query, (user_id, message, datetime.datetime.now()))

    def clean_old_messages(self, hours=24):
        """Deletes messages older than the specified number of hours."""
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
        query = "DELETE FROM chats WHERE timestamp < %s"
        self.execute_query(query, (cutoff_time,))
        print(f"Deleted messages older than {hours} hours.")

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

# Initialize the database connection
db = DatabaseConnection()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')  # Extract user message
    print(f"Received user input: {user_input}")  # Debug log
    
    # Save user input to the database
    db.add_message("User", user_input)
    
    # Get bot response
    bot_response = get_bot_response(user_input)
    
    # Save bot response to the database
    db.add_message("Bot", bot_response)
    
    # Remove markdown characters from the response
    clean_response = strip_markdown(bot_response)
    
    # Format the response with code blocks
    formatted_response = format_code_blocks(clean_response)
    
    return jsonify({"response": formatted_response})

def periodic_cleanup():
    """Periodically cleans old messages from the database."""
    while True:
        db.clean_old_messages(hours=48)  # Clean messages older than 24 hours
        time.sleep(3600)  # Run every hour (3600 seconds)

if __name__ == '__main__':
    # Start the periodic cleanup in a separate thread
    cleanup_thread = threading.Thread(target=periodic_cleanup, daemon=True)
    cleanup_thread.start()
    
    # Run the Flask app
    app.run(debug=True)
