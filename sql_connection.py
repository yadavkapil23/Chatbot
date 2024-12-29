import mysql.connector
import datetime
import time
import threading
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'kapil')
DB_NAME = os.getenv('DB_NAME', 'Neobot')


class DatabaseConnection:
    """Handles the MySQL database connection."""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establishes a database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.cursor = self.connection.cursor()
            print("Database connection established.")
        except Error as e:
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
        except Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query, params=None):
        """Fetches all results from a query."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []


def setup_db(db):
    """Initializes the database and creates the chats table."""
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS chats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            message TEXT,
            timestamp DATETIME
        )
    '''
    db.execute_query(create_table_query)
    print("Database setup completed.")


def add_message(db, user_id, message):
    """Adds a message to the database."""
    insert_query = "INSERT INTO chats (user_id, message, timestamp) VALUES (%s, %s, %s)"
    print(f"Executing query: {insert_query} with values: ({user_id}, {message}, {datetime.datetime.now()})")
    db.execute_query(insert_query, (user_id, message, datetime.datetime.now()))
    print(f"Message added: {user_id} - {message}")



def clean_old_messages(db, hours=24):
    """Deletes messages older than the specified number of hours."""
    cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
    delete_query = "DELETE FROM chats WHERE timestamp < %s"
    db.execute_query(delete_query, (cutoff_time,))
    print(f"Deleted messages older than {hours} hours.")


def periodic_clean(db, interval=3600):
    """Periodically cleans old messages."""
    while True:
        clean_old_messages(db)
        print(f"Cleaned old messages at {datetime.datetime.now()}")
        time.sleep(interval)


def main():
    """Main function for the chatbot simulation."""
    db = DatabaseConnection()
    db.connect()

    # Set up the database
    setup_db(db)

    # Simulate adding messages
    for i in range(10):
        add_message(db, user_id=f"User_{i}", message=f"Message number {i}")
        time.sleep(1)

    # Start periodic cleaning in a separate thread
    clean_thread = threading.Thread(target=periodic_clean, args=(db, 10))  # 10-second interval for testing
    clean_thread.daemon = True
    clean_thread.start()

    # Keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        db.disconnect()


if __name__ == "__main__":
    main()
