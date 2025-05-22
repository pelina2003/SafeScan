import sqlite3

conn = sqlite3.connect("data/dummy_data.db")
cursor = conn.cursor()

# Επαναφορά πρώτων 6 αναφορών ως confirmed
cursor.execute("UPDATE reports SET status = 'confirmed' WHERE id <= 6")
conn.commit()
conn.close()

print("✅ Επαναφέρθηκαν οι πρώτες 6 αναφορές ως 'confirmed'")
