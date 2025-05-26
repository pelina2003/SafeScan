# init_db.py
import sqlite3
import os

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/dummy_data.db")
cursor = conn.cursor()

# Δημιουργία πίνακα reports
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    status TEXT CHECK(status IN ('pending', 'confirmed')) NOT NULL DEFAULT 'pending'
)
""")

# Δείγματα μόνο αν η βάση είναι άδεια
cursor.execute("SELECT COUNT(*) FROM reports")
count = cursor.fetchone()[0]

if count == 0:
    sample_data = [
        ("Πυρκαγιά", 37.9838, 23.7275, "confirmed"),
        ("Πλημμύρα", 38.2466, 21.7346, "confirmed"),
        ("Ατύχημα", 40.6401, 22.9444, "confirmed")
    ]
    cursor.executemany("INSERT INTO reports (type, latitude, longitude, status) VALUES (?, ?, ?, ?)", sample_data)
    print("✅ Προστέθηκαν επιβεβαιωμένα δείγματα στη βάση.")
else:
    print("ℹ️ Η βάση περιέχει ήδη δεδομένα.")

conn.commit()
conn.close()
