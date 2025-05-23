import sqlite3

conn = sqlite3.connect("data/dummy_data.db")
cursor = conn.cursor()

cursor.execute("UPDATE reports SET status = 'pending'")
conn.commit()
conn.close()

print("✅ Όλες οι αναφορές έγιναν 'pending'")
