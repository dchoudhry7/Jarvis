import sqlite3

conn = sqlite3.connect(
    "jarvis.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory TEXT NOT NULL
)
""")

conn.commit()
