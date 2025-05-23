import sqlite3

DB_PATH = "data/dummy_data.db"

def get_confirmed_reports():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, type, latitude, longitude 
            FROM reports 
            WHERE status = 'confirmed'
        """)
        
        results = cursor.fetchall()
        conn.close()
        return results

    except Exception as e:
        print(f"⚠️ Σφάλμα βάσης: {e}")
        return None
