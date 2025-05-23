import sqlite3

conn = sqlite3.connect("data/dummy_data.db")
cursor = conn.cursor()

# Επίλεξε μία επιβεβαιωμένη αναφορά και "χαλάς" τα γεωγραφικά της δεδομένα
cursor.execute("""
    UPDATE reports
    SET latitude = NULL, longitude = NULL
    WHERE id = (SELECT id FROM reports WHERE status='confirmed' LIMIT 1)
""")

conn.commit()
conn.close()

print("⚠️ Μία επιβεβαιωμένη αναφορά έχει τώρα άκυρα γεωγραφικά δεδομένα.")
