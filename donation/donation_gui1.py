import tkinter as tk
from tkinter import messagebox

# Λίστα επιλογών για δωρεά (μπορείς να προσαρμόσεις τα ονόματα σύμφωνα με τα mockups σου)
donation_options = [
    "Αναδάσωση στην πλαγιά της Πεντέλης",
    "Συλλογή απορριμμάτων στην παραλία Νέας Μάκρης",
    "Οργανισμός προστασίας θαλάσσιας χελώνας"
]

# Η μεταβλητή όπου θα αποθηκευτεί η επιλογή του χρήστη
selected_option = None

# Συνάρτηση που καλείται όταν ο χρήστης επιλέγει μια από τις επιλογές
def select_option(option):
    global selected_option
    selected_option = option
    open_donation_window()

# Συνάρτηση που ανοίγει το παράθυρο για την εισαγωγή ποσού και επιβεβαίωση δωρεάς
def open_donation_window():
    window.destroy()  # Κλείνουμε το κύριο παράθυρο επιλογής

    donation_window = tk.Tk()
    donation_window.title("Δωρεά")

    # Τίτλος και οδηγίες
    tk.Label(donation_window, text="Εισαγάγετε το ποσό της δωρεάς", font=("Arial", 14)).pack(pady=10)

    # Πεδίο εισαγωγής ποσού
    amount_entry = tk.Entry(donation_window, width=20, font=("Arial", 12))
    amount_entry.pack(pady=5)

    # Εμφάνιση της επιλεγμένης δράσης/οργανισμού
    tk.Label(donation_window, text="Επιλεγμένη Δράση / Οργανισμός:", font=("Arial", 10)).pack(pady=5)
    tk.Label(donation_window, text=selected_option, font=("Arial", 10, "bold")).pack(pady=5)

    # Συνάρτηση που καλείται για να επιβεβαιώσει τη δωρεά
    def confirm_donation():
        try:
            # Ανάγνωση και έλεγχος ποσού (η τιμή 1000 είναι παράδειγμα ανώτατου ορίου)
            amount = float(amount_entry.get())
            if amount <= 0 or amount > 1000:
                raise ValueError
            messagebox.showinfo("Επιτυχία", f"✅ Δωρεά {amount}€ για: {selected_option}")
            donation_window.destroy()
        except ValueError:
            messagebox.showerror("Σφάλμα", "❌ Το ποσό δεν είναι έγκυρο. Επιλέξτε ποσό μεταξύ 0 και 1000€.")

    # Συνάρτηση για ακύρωση της δωρεάς
    def cancel_donation():
        messagebox.showinfo("Ακύρωση", "Η δωρεά ακυρώθηκε.")
        donation_window.destroy()

    # Κουμπιά Επιβεβαίωσης και Ακύρωσης, τοποθετημένα μέσα σε ένα πλαίσιο
    button_frame = tk.Frame(donation_window)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Επιβεβαίωση", command=confirm_donation, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Ακύρωση", command=cancel_donation, font=("Arial", 12)).pack(side=tk.RIGHT, padx=10)

    donation_window.mainloop()

# Δημιουργία του κύριου παραθύρου για επιλογή δράσης/οργανισμού
window = tk.Tk()
window.title("Επιλογή Δράσης/Οργανισμού")

tk.Label(window, text="Επιλέξτε μια δράση ή οργανισμό για δωρεά", font=("Arial", 14)).pack(pady=10)

# Δημιουργούμε ένα κουμπί για κάθε επιλογή στη λίστα donation_options
for option in donation_options:
    tk.Button(window, text=option, width=50, command=lambda opt=option: select_option(opt), font=("Arial", 12)).pack(pady=5)

window.mainloop()
