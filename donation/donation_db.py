import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# === Δημιουργία ή σύνδεση με τη βάση δεδομένων ===

def setup_database():
    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS social_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT,
        location TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        target_type TEXT NOT NULL,
        target_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        payment_method TEXT,
        user_name TEXT,
        date TEXT NOT NULL
    )
    """)

    # Εισαγωγή δείγματος αν είναι άδεια
    cursor.execute("SELECT COUNT(*) FROM social_actions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO social_actions (title, category, location) VALUES (?, ?, ?)", [
            ("Αναδάσωση στην πλαγιά της Πεντέλης", "Περιβάλλον", "Αττική"),
            ("Συλλογή απορριμμάτων στην παραλία Νέας Μάκρης", "Καθαριότητα", "Αττική")
        ])

    cursor.execute("SELECT COUNT(*) FROM organizations")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO organizations (name, category) VALUES (?, ?)", [
            ("Οργανισμός προστασίας θαλάσσιας χελώνας", "Θάλασσα"),
            ("Εταιρεία αναδάσωσης Ελλάδας", "Δάση")
        ])

    conn.commit()
    conn.close()

# === Συνάρτηση για ανάγνωση διαθέσιμων επιλογών δωρεάς ===

def get_donation_options():
    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()
    options = []

    cursor.execute("SELECT id, title FROM social_actions")
    for row in cursor.fetchall():
        options.append(("action", row[0], row[1]))

    cursor.execute("SELECT id, name FROM organizations")
    for row in cursor.fetchall():
        options.append(("organization", row[0], row[1]))

    conn.close()
    return options

# === Συνάρτηση για καταχώρηση δωρεάς ===

def save_donation(amount, target_type, target_id, status, payment_method, user_name):
    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO donations (amount, target_type, target_id, status, payment_method, user_name, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (amount, target_type, target_id, status, payment_method, user_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# === GUI ΛΟΓΙΚΗ ===

selected_option = None

def select_option(option):
    global selected_option
    selected_option = option
    open_donation_window()

def open_donation_window():
    window.destroy()

    donation_window = tk.Tk()
    donation_window.title("Δωρεά")

    tk.Label(donation_window, text="Εισαγάγετε το ποσό της δωρεάς (€):").pack(pady=10)
    amount_entry = tk.Entry(donation_window)
    amount_entry.pack(pady=5)

    tk.Label(donation_window, text=f"Προς: {selected_option[2]}").pack(pady=5)

    def confirm_donation():
        try:
            amount = float(amount_entry.get())
            if amount <= 0 or amount > 1000:
                raise ValueError
            save_donation(amount, selected_option[0], selected_option[1], "CONFIRMED", "Κάρτα", "giannis")
            messagebox.showinfo("Επιτυχία", f"✅ Δωρεά {amount}€ καταχωρήθηκε για: {selected_option[2]}")
            donation_window.destroy()
        except ValueError:
            messagebox.showerror("Σφάλμα", "❌ Το ποσό δεν είναι έγκυρο. Επιλέξτε ποσό μεταξύ 0 και 1000€.")

    def cancel_donation():
        messagebox.showinfo("Ακύρωση", "Η δωρεά ακυρώθηκε.")
        donation_window.destroy()

    tk.Button(donation_window, text="Επιβεβαίωση", command=confirm_donation).pack(side=tk.LEFT, padx=20, pady=10)
    tk.Button(donation_window, text="Ακύρωση", command=cancel_donation).pack(side=tk.RIGHT, padx=20, pady=10)

    donation_window.mainloop()

# === Εκκίνηση εφαρμογής ===

setup_database()
options = get_donation_options()

window = tk.Tk()
window.title("Κοινωνική Δράση/Οργανισμός")

tk.Label(window, text="Επιλέξτε μια επιλογή για να κάνετε δωρεά", font=('Arial', 12)).pack(pady=10)

for opt in options:
    tk.Button(window, text=opt[2], width=50, command=lambda o=opt: select_option(o)).pack(pady=5)

window.mainloop()
