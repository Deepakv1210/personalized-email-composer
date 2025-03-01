import sqlite3
import hashlib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = "emails_secure.db"
SECRET_KEY = os.getenv("SECRET_KEY")  # Load secret key from .env

def hash_password(password):
    """Hashes a password using SHA-256 for simple security."""
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_database():
    """Creates a SQLite database if it doesn't exist."""
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Create emails table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                greeting TEXT,
                body TEXT,
                closing TEXT
            );
        """)

        conn.commit()
        conn.close()

def insert_email(subject, greeting, body, closing):
    """Inserts an email into the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO emails (subject, greeting, body, closing)
        VALUES (?, ?, ?, ?);
    """, (subject, greeting, body, closing))

    conn.commit()
    conn.close()

def fetch_all_emails():
    """Retrieves all stored emails."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT subject, greeting, body, closing FROM emails;")
    emails = cursor.fetchall()
    
    conn.close()
    return emails

# Initialize DB on first run
initialize_database()

if __name__ == "__main__":
    emails = fetch_all_emails()
    for email in emails:
        print("\n--- Stored Email ---")
        print("Subject:", email[0])
        print("Greeting:", email[1])
        print("Body:", email[2])
        print("Closing:", email[3])