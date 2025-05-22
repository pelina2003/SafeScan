import tkinter as tk
from tkinter import messagebox
import sqlite3
from message_manager import get_messages_for_forum, add_message

DB_PATH = "../map_code/data/dummy_data.db"

def get_forum_list():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, latitude, longitude, created_at FROM forums ORDER BY created_at DESC")
        forums = cursor.fetchall()
        conn.close()
        return forums
    except Exception as e:
        print("Σφάλμα σύνδεσης με βάση:", e)
        return None

def open_forum_window(forum_id):
    window = tk.Toplevel()
    window.title(f"Φόρουμ #{forum_id}")
    window.geometry("600x500")

    tk.Label(window, text=f"Μηνύματα στο Φόρουμ #{forum_id}:", font=("Arial", 12, "bold")).pack(pady=5)

    messages_box = tk.Text(window, width=70, height=20, state='disabled')
    messages_box.pack(pady=5)

    def load_messages():
        messages = get_messages_for_forum(forum_id)
        messages_box.configure(state='normal')
        messages_box.delete(1.0, tk.END)
        for msg, timestamp in messages:
            messages_box.insert(tk.END, f"[{timestamp}]\n{msg}\n\n")
        messages_box.configure(state='disabled')

    load_messages()

    entry = tk.Entry(window, width=60)
    entry.pack(pady=5)

    def submit_message():
        content = entry.get().strip()
        if not content:
            messagebox.showwarning("Προσοχή", "Το μήνυμα δεν μπορεί να είναι κενό.")
            return
        success = add_message(forum_id, content)
        if success:
            entry.delete(0, tk.END)
            load_messages()
        else:
            messagebox.showerror("Σφάλμα", "Το μήνυμα δεν αποθηκεύτηκε. Παρακαλώ προσπαθήστε ξανά.")

    send_button = tk.Button(window, text="Αποστολή", command=submit_message)
    send_button.pack(pady=5)

def open_forum_gui():
    root = tk.Tk()
    root.title("Λίστα Φόρουμ Συζητήσεων")
    root.geometry("600x400")

    forums = get_forum_list()
    if forums is None:
        messagebox.showerror("Σφάλμα", "Αποτυχία φόρτωσης φόρουμ. Προσπαθήστε ξανά.")
        return

    if len(forums) == 0:
        messagebox.showinfo("Πληροφορία", "Δεν υπάρχουν διαθέσιμα φόρουμ προς το παρόν.")
        return

    label = tk.Label(root, text="Επιλέξτε ένα φόρουμ από τη λίστα:", font=("Arial", 12))
    label.pack(pady=10)

    listbox = tk.Listbox(root, width=80, height=15)
    for forum in forums:
        forum_id, ftype, lat, lon, created = forum
        listbox.insert(tk.END, f"#{forum_id} | {ftype} | ({lat:.4f}, {lon:.4f}) | {created}")
    listbox.pack(pady=10)

    def on_select():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Προσοχή", "Παρακαλώ επιλέξτε ένα φόρουμ.")
            return
        selected_forum = forums[selected_index[0]]
        forum_id = selected_forum[0]
        open_forum_window(forum_id)

    select_button = tk.Button(root, text="Άνοιγμα Φόρουμ", command=on_select)
    select_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    open_forum_gui()
