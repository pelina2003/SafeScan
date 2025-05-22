import sqlite3

DB_PATH = "../map_code/data/dummy_data.db"
PROXIMITY_THRESHOLD = 0.02

def create_forum_if_not_exists(report):
    report_id, r_type, lat, lon = report

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM forums
            WHERE type = ?
              AND ABS(latitude - ?) < ?
              AND ABS(longitude - ?) < ?
        """, (r_type, lat, PROXIMITY_THRESHOLD, lon, PROXIMITY_THRESHOLD))

        existing = cursor.fetchone()

        if existing:
            forum_id = existing[0]
            print(f"⚠️ Αναφορά #{report_id} σχετίζεται με υπάρχον φόρουμ #{forum_id} (κοντινή τοποθεσία).")
            return

        cursor.execute("""
            INSERT INTO forums (report_id, type, latitude, longitude)
            VALUES (?, ?, ?, ?)
        """, (report_id, r_type, lat, lon))
        conn.commit()
        print(f"✅ Δημιουργήθηκε νέο φόρουμ για αναφορά #{report_id}")

    except Exception as e:
        print(f"❌ Σφάλμα κατά τη δημιουργία φόρουμ: {e}")
    finally:
        conn.close()

def scan_reports_and_create_forums():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, latitude, longitude FROM reports WHERE status = 'confirmed'")
        confirmed_reports = cursor.fetchall()
        conn.close()

        print(f"🔍 Βρέθηκαν {len(confirmed_reports)} επιβεβαιωμένες αναφορές.")
        for report in confirmed_reports:
            create_forum_if_not_exists(report)

    except Exception as e:
        print(f"❌ Σφάλμα κατά τον έλεγχο αναφορών: {e}")
