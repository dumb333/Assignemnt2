from xmlrpc.server import SimpleXMLRPCServer
import sqlite3
import logging
import requests
from hashlib import sha256

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the SQLite database
db_path = "notebook.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS notes
             (topic text, text text, timestamp text)''')
conn.commit()

# User credentials
users = {"admin": sha256("password".encode()).hexdigest()}

# Function to check credentials
def check_credentials(username, password):
    if username in users and users[username] == sha256(password.encode()).hexdigest():
        return True
    return False

# Server functions with exception handling
def add_note(topic, text, timestamp, username, password):
    if not check_credentials(username, password):
        return "Authentication failed"
    try:
        c.execute("INSERT INTO notes (topic, text, timestamp) VALUES (?, ?, ?)", (topic, text, timestamp))
        conn.commit()
        return f"Note added to {topic}"
    except Exception as e:
        logging.error("Error adding note: %s", e)
        return "An error occurred"

def get_notes(topic, username, password):
    if not check_credentials(username, password):
        return "Authentication failed"
    try:
        c.execute("SELECT text, timestamp FROM notes WHERE topic=?", (topic,))
        notes = [{"text": row[0], "timestamp": row[1]} for row in c.fetchall()]
        return notes if notes else "No notes found for this topic"
    except Exception as e:
        logging.error("Error retrieving notes: %s", e)
        return "An error occurred"

def search_wikipedia(topic, username, password):
    if not check_credentials(username, password):
        return "Authentication failed"
    try:
        base_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": topic,
            "limit": "1",
            "namespace": "0",
            "format": "json"
        }

        response = requests.get(base_url, params=params).json()
        if response[1]:
            return {"title": response[1][0], "url": response[3][0]}
        else:
            return "No Wikipedia article found."
    except Exception as e:
        logging.error("Error searching Wikipedia: %s", e)
        return "An error occurred during Wikipedia search"

# Server setup
server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(add_note, "add_note")
server.register_function(get_notes, "get_notes")
server.register_function(search_wikipedia, "search_wikipedia")  # Make sure this line is present

# Serve forever
try:
    server.serve_forever()
except Exception as e:
    logging.error("Server error: %s", e)
finally:
    conn.close()


