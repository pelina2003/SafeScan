import sqlite3

DB_PATH = "../map_code/data/dummy_data.db"

def get_messages_for_forum(forum_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT content, timestamp FROM messages
        WHERE forum_id = ?
        ORDER BY timestamp ASC
    """, (forum_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

def add_message(forum_id, content):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (forum_id, content)
            VALUES (?, ?)
        """, (forum_id, content))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("❌ Σφάλμα αποθήκευσης μηνύματος:", e)
        return False
