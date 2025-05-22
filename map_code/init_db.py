import sqlite3
import os

# Δημιουργία φακέλου data αν δεν υπάρχει
os.makedirs("data", exist_ok=True)

# Σύνδεση στη βάση δεδομένων
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

# Προσθήκη δειγμάτων αν ο πίνακας είναι άδειος
cursor.execute("SELECT COUNT(*) FROM reports")
count = cursor.fetchone()[0]

if count == 0:
    sample_data = [
        ("Πυρκαγιά", 37.9838, 23.7275, "pending"),
        ("Πλημμύρα", 38.2466, 21.7346, "pending"),
        ("Καθαρισμός", 37.9838, 23.7275, "pending"),
        ("Ατύχημα", 40.6401, 22.9444, "pending")
    ]
    cursor.executemany("INSERT INTO reports (report_type, latitude, longitude, status) VALUES (?, ?, ?, ?)", sample_data)
    print("✅ Η βάση δημιουργήθηκε με δείγματα.")
else:
    print("ℹ️ Η βάση υπάρχει ήδη με δεδομένα.")

conn.commit()
conn.close()
