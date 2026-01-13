import sqlite3
import os
import time
from .config import Config

class DatabaseManager:
    def __init__(self):
        # Store db in the same dir as config or user home
        # For now, let's put it in the base dir
        self.db_path = os.path.join(Config.BASE_DIR, "hexstrike_nexus.db")
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      role TEXT,
                      message TEXT,
                      timestamp REAL,
                      agent TEXT)''')
        conn.commit()
        conn.close()

    def add_message(self, role, message, agent="System"):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO chat_history (role, message, timestamp, agent) VALUES (?, ?, ?, ?)",
                  (role, message, time.time(), agent))
        conn.commit()
        conn.close()

    def get_history(self, limit=50):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT role, message, agent, timestamp FROM chat_history ORDER BY timestamp ASC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        return rows
