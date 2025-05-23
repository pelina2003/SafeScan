import sqlite3

conn = sqlite3.connect("data/dummy_data.db")
cursor = conn.cursor()

# Επαναφορά γεωγραφικών συντεταγμένων για την πρώτη επιβεβαιωμένη αναφορά
cursor.execute("""
    UPDATE reports
    SET latitude = 37.9838, longitude = 23.7275
    WHERE latitude IS NULL OR longitude IS NULL
""")

conn.commit()
conn.close()

print("✅ Επαναφέρθηκαν γεωγραφικά δεδομένα σε όλες τις αναφορές.")
