import sqlite3

def init_forum_table():
    conn = sqlite3.connect("../map_code/data/dummy_data.db")
    cursor = conn.cursor()

    # 👉 Διαγραφή του πίνακα (αν υπάρχει)
    cursor.execute("DROP TABLE IF EXISTS forums")

    # 👉 Δημιουργία πίνακα με το σωστό schema
    cursor.execute("""
        CREATE TABLE forums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        forum_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (forum_id) REFERENCES forums(id)
    )
""")


    conn.commit()
    conn.close()
    print("✅ Ο πίνακας 'forums' δημιουργήθηκε (ή επαναδημιουργήθηκε).")

if __name__ == "__main__":
    init_forum_table()

