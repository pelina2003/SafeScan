# init_db.py
import sqlite3
import os

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/dummy_data.db")
cursor = conn.cursor()

# Πίνακας forums
cursor.execute("""
CREATE TABLE IF NOT EXISTS forums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    risk_type TEXT NOT NULL,
    location TEXT,
    latitude REAL,
    longitude REAL,
    created_at TEXT NOT NULL
)
""")

# Πίνακας messages
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    forum_id INTEGER NOT NULL,
    FOREIGN KEY(forum_id) REFERENCES forums(id)
)
""")

# Προσθήκη παραδειγμάτων (αν δεν υπάρχουν ήδη)
cursor.execute("SELECT COUNT(*) FROM forums")
forum_count = cursor.fetchone()[0]

if forum_count == 0:
    print("➕ Δημιουργία δειγμάτων...")
    cursor.execute("""
        INSERT INTO forums (topic, risk_type, location, latitude, longitude, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Συζήτηση για Πλημμύρα", "Πλημμύρα", "38.0,21.8", 38.0, 21.8, "2025-05-26T12:00:00"))

    forum_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO messages (content, author, timestamp, forum_id)
        VALUES (?, ?, ?, ?)
    """, ("Κάτοικος: Υπάρχει σοβαρό πρόβλημα στην περιοχή!", "Maria", "2025-05-26T12:05:00", forum_id))

    print("✅ Εισαγωγή δείγματος φόρουμ & μηνύματος")

else:
    print("ℹ️ Η βάση περιέχει ήδη φόρουμ.")

conn.commit()
conn.close()
