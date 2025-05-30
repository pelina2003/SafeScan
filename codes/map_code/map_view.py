# map_view.py
import tkinter as tk
from tkinter import messagebox
import webbrowser
from map_controller import MapController

class MapView:
    def __init__(self, user=None):
        self.controller = MapController()
        self.root = tk.Tk()
        self.root.title("SafeScan - Χάρτης Κινδύνων")
        self.root.geometry("400x250")

        label = tk.Label(self.root, text="Καλώς ήρθες στο SafeScan", font=("Arial", 14))
        label.pack(pady=20)

        btn_map = tk.Button(self.root, text="🗺️ Προβολή Χάρτη Κινδύνων", command=self.show_risk_map)
        btn_map.pack(pady=10)

        self.reload_button = tk.Button(self.root, text="🔁 Επαναφόρτωση", command=self.reload_map)
        self.reload_button.pack(pady=5)

        self.root.mainloop()

    def show_risk_map(self):
        self._handle_map_generation()

    def reload_map(self):
        self._handle_map_generation()

    def _handle_map_generation(self):
        result = self.controller.update_map()
        if result == "db_error":
            messagebox.showerror("Σφάλμα Βάσης", "Αποτυχία φόρτωσης δεδομένων.\nΠροσπαθήστε ξανά αργότερα.")
        elif result == "no_reports":
            messagebox.showinfo("Πληροφορία", "Δεν υπάρχουν επιβεβαιωμένοι κίνδυνοι προς το παρόν.")
        elif result == "partial_data":
            messagebox.showwarning("Μερική Εμφάνιση", "Ορισμένοι κίνδυνοι δεν εμφανίστηκαν λόγω ελλιπών δεδομένων.")
        elif result == "ok":
            messagebox.showinfo("Επιτυχία", "Ο χάρτης κινδύνων δημιουργήθηκε με επιτυχία.")
        else:
            messagebox.showerror("Άγνωστο Σφάλμα", "Κάτι πήγε στραβά κατά την δημιουργία του χάρτη.")
        webbrowser.open("risk_map.html")
