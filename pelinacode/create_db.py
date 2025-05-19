import sqlite3

def create_confirmed_reports_table(db_name="safescan.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Δημιουργία πίνακα confirmed_reports (αν δεν υπάρχει ήδη)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS confirmed_reports (
            id TEXT PRIMARY KEY,
            category TEXT,
            region TEXT,
            date TEXT,
            status TEXT
        )
    """)

    # Δείγματα επιβεβαιωμένων αναφορών για τα στατιστικά
    sample_data = [
        ("CONF001", "Πυρκαγιές", "Αθήνα", "2023-01", "confirmed"),
        ("CONF002", "Κοινωνικά Ζητήματα", "Πάτρα", "2023-02", "confirmed"),
        ("CONF003", "Εγκληματικότητα", "Θεσσαλονίκη", "2023-01", "confirmed"),
        ("CONF004", "Πυρκαγιές", "Πάτρα", "2023-03", "confirmed"),
        ("CONF005", "Φυσικές Καταστροφές", "Αθήνα", "2023-02", "confirmed"),
        ("CONF006", "Πυρκαγιές", "Πάτρα", "2023-02", "confirmed"),
        ("CONF007", "Πυρκαγιές", "Πάτρα", "2023-01", "confirmed"),
        ("CONF008", "Εγκληματικότητα", "Αθήνα", "2023-03", "confirmed"),
    ]

    # Εισαγωγή δεδομένων (αγνόηση διπλοεγγραφών)
    for row in sample_data:
        try:
            cursor.execute("INSERT INTO confirmed_reports VALUES (?, ?, ?, ?, ?)", row)
        except sqlite3.IntegrityError:
            pass  # αγνοεί αν το id υπάρχει ήδη

    conn.commit()
    conn.close()
    print("Ο πίνακας 'confirmed_reports' δημιουργήθηκε και περιέχει εγκεκριμένες αναφορές.")

# Εκτέλεση
create_confirmed_reports_table()
