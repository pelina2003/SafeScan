import tkinter as tk
from tkinter import messagebox
import webbrowser
from map_display import create_risk_map

def show_risk_map():
    result = create_risk_map()

    if result == "db_error":
        messagebox.showerror("Σφάλμα Βάσης", "Αποτυχία φόρτωσης δεδομένων.\nΠροσπαθήστε ξανά αργότερα.")
        return
    elif result == "no_reports":
        messagebox.showinfo("Πληροφορία", "Δεν υπάρχουν επιβεβαιωμένοι κίνδυνοι προς το παρόν.")
    elif result == "partial_data":
        messagebox.showwarning("Μερική Εμφάνιση", "Ορισμένοι κίνδυνοι δεν εμφανίστηκαν λόγω ελλιπών δεδομένων.")
    elif result == "ok":
        messagebox.showinfo("Επιτυχία", "Ο χάρτης κινδύνων δημιουργήθηκε με επιτυχία.")
    else:
        messagebox.showerror("Άγνωστο Σφάλμα", "Κάτι πήγε στραβά κατά την δημιουργία του χάρτη.")

    # Άνοιγμα HTML χάρτη
    webbrowser.open("risk_map.html")

# Δημιουργία GUI
root = tk.Tk()
root.title("SafeScan - Αρχική Σελίδα")
root.geometry("400x200")

label = tk.Label(root, text="Καλώς ήρθες στο SafeScan", font=("Arial", 14))
label.pack(pady=20)

btn_map = tk.Button(root, text="Χάρτης Κινδύνων", command=show_risk_map)
btn_map.pack(pady=20)

root.mainloop()
