from report import Report
import sqlite3

DB_PATH = "data/dummy_data.db"

class DBManager:
    @staticmethod
    def get_confirmed_reports():
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, type, latitude, longitude, status 
                FROM reports 
                WHERE status = 'confirmed'
            """)
            rows = cursor.fetchall()
            conn.close()
            return [Report(*row) for row in rows]
        except Exception as e:
            print(f"⚠️ Σφάλμα βάσης: {e}")
            return None
