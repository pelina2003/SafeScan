# db_manager.py
import sqlite3
from forum import Forum
from message import Message
from datetime import datetime

DB_PATH = "data/dummy_data.db"

class DBManager:

    @staticmethod
    def get_all_forums():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, topic, risk_type, location, created_at FROM forums ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [Forum(*row) for row in rows]

    @staticmethod
    def find_similar_forum(risk_type, latitude, longitude):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Εύρεση κοντινού forum (π.χ. με +/- 0.01 στις συντεταγμένες)
        cursor.execute("""
            SELECT id, topic, risk_type, location, created_at FROM forums
            WHERE risk_type = ?
            AND ABS(latitude - ?) < 0.01 AND ABS(longitude - ?) < 0.01
            LIMIT 1
        """, (risk_type, latitude, longitude))
        row = cursor.fetchone()
        conn.close()
        return Forum(*row) if row else None

    @staticmethod
    def create_forum(report):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            topic = f"Συζήτηση για {report.type}"
            location = f"{round(report.latitude, 3)},{round(report.longitude, 3)}"
            created_at = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO forums (topic, risk_type, location, latitude, longitude, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (topic, report.type, location, report.latitude, report.longitude, created_at))
            conn.commit()
            forum_id = cursor.lastrowid
            conn.close()
            return Forum(forum_id, topic, report.type, location, created_at)
        except Exception as e:
            print(f"⚠️ Σφάλμα δημιουργίας φόρουμ: {e}")
            return None

    @staticmethod
    def get_forum_messages(forum_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, content, author, timestamp, forum_id FROM messages
            WHERE forum_id = ? ORDER BY timestamp
        """, (forum_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Message(*row) for row in rows]

    @staticmethod
    def save_message(forum_id, author, content):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            timestamp = datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO messages (content, author, timestamp, forum_id)
                VALUES (?, ?, ?, ?)
            """, (content, author, timestamp, forum_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"⚠️ Σφάλμα αποθήκευσης μηνύματος: {e}")
            return False
