import sqlite3

# Σύνδεση με τη βάση
conn = sqlite3.connect("data/dummy_data.db")
cursor = conn.cursor()

# Αλλαγή όλων των αναφορών σε 'pending'
cursor.execute("UPDATE reports SET status = 'pending'")
conn.commit()
conn.close()

print("✅ Όλες οι αναφορές έγιναν 'pending'")
