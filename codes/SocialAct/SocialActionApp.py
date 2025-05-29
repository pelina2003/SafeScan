import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from typing import List, Tuple

from user import User
from report import Report
from social_action_form import SocialActionForm
from socialAction import SocialAction
from donation import DonationPool


class SocialActionApp:
    PAD = 10

    def __init__(self, root):
        self._root = root
        self._root.title("Κοινωνικές Δράσεις")
        self._root.geometry("500x450")
        self._current_user = User(1, "test_user")

        self._reports = [
            Report(1, "Κατεστραμμένη παιδική χαρά", "Υποδομές"),
            Report(2, "Σκουπίδια στο πάρκο", "Περιβάλλον"),
            Report(3, "Σπασμένη λάμπα σε δρόμο", "Ηλεκτροφωτισμός"),
            Report(4, "Διαρροή νερού σε δημόσιο χώρο", "Ύδρευση"),
        ]


        self._pool = DonationPool()
        self._style = ttk.Style()
        self._style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        self._style.configure("TFrame", padding=self.PAD)
        self.build_main_menu()

    def clear_frame(self):
        for w in self._root.winfo_children():
            w.destroy()

    def header(self, parent, text):
        ttk.Label(parent, text=text, style="Header.TLabel").pack(pady=(0, self.PAD))

    def status_bar(self):
        count = SocialAction.active_count()
        lbl = ttk.Label(self._root, text=f"Ενεργές Δράσεις: {count}", foreground="#2a7f62")
        lbl.pack(side="bottom", fill="x", pady=(0, self.PAD))

    def build_main_menu(self):
        self.clear_frame()
        frm = ttk.Frame(self._root)
        frm.pack(fill="both", expand=True)

        self.header(frm, "Καλωσήρθες!")
        ttk.Button(frm, text="Δημιουργία Κοινωνικής Δράσης",
                   command=self.show_risk_selection).pack(pady=self.PAD)
        self.status_bar()

    def show_risk_selection(self):
        if not SocialAction.can_create_action():
            messagebox.showwarning("Προσοχή", "Υπερβήθηκε το μέγιστο όριο ενεργών δράσεων.")
            return
        if not self._reports:
            messagebox.showinfo("Πληροφορία", "Δεν υπάρχουν διαθέσιμες αναφορές κινδύνων.")
            if SocialAction.active_count() > 0:
                self._root.after(2000, self.show_active_actions)  # Delay for "Μετάβαση στις ενεργές δράσεις"
            return
        self.clear_frame()
        frm = ttk.Frame(self._root)
        frm.pack(fill="both", expand=True)

        self.header(frm, "Επιλογή Αναφοράς Κινδύνου")
        self._risk_var = tk.StringVar()
        for report in self._reports:
            ttk.Radiobutton(frm, text=report._name, variable=self._risk_var, value=report._name).pack(anchor="w")
        ttk.Button(frm, text="Επόμενο", command=self.show_form).pack(pady=self.PAD)
        self.status_bar()

    def show_active_actions(self):
        #Use-Case 5: Display active actions
        messagebox.showinfo("Πληροφορία", "Μετάβαση στις ενεργές δράσεις.")
        self.build_main_menu()  #Temporary back to main menu

    def show_form(self):
        selected = self._risk_var.get()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επιλέξτε αναφορά κινδύνου.")
            return
        selected_report = None
        for report in self._reports:
            if report._name == selected:
                selected_report = report
                break
        if not selected_report:
            messagebox.showwarning("Προσοχή", "Η επιλεγμένη αναφορά κινδύνου δεν είναι έγκυρη.")
            return

        self._selected_report = selected_report
        self.clear_frame()
        frm = ttk.Frame(self._root)
        frm.pack(fill="both", expand=True)

        self.header(frm, f"Αναφορά Κινδύνου: {self._selected_report._name}")

        form_frame = ttk.LabelFrame(frm, text="Στοιχεία Δράσης")
        form_frame.pack(fill="both", expand=True, pady=self.PAD)

        ttk.Label(form_frame, text="Περιγραφή:").grid(row=0, column=0, sticky="e", padx=self.PAD, pady=5)
        self.e_desc = ttk.Entry(form_frame, width=40)
        self.e_desc.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Ημ/νία (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=self.PAD, pady=5)
        self.e_date = ttk.Entry(form_frame)
        self.e_date.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Τοποθεσία:").grid(row=2, column=0, sticky="e", padx=self.PAD, pady=5)
        self.e_loc = ttk.Entry(form_frame, width=40)
        self.e_loc.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Απαιτούμενο ποσό (€):").grid(row=3, column=0, sticky="e", padx=self.PAD, pady=5)
        self.e_amt = ttk.Entry(form_frame)
        self.e_amt.grid(row=3, column=1, pady=5)

        ttk.Button(frm, text="Ολοκλήρωση", command=self.submit).pack(pady=self.PAD)
        self.status_bar()

    def submit(self):
        desc = self.e_desc.get().strip()
        if not desc:
            messagebox.showerror("Σφάλμα", "Η περιγραφή δεν μπορεί να είναι κενή.")
            return

        date_str = self.e_date.get().strip()
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            if dt.date() <= datetime.now().date():
                messagebox.showerror("Σφάλμα", "Η ημερομηνία πρέπει να είναι στο μέλλον.")
                return
        except ValueError:
            messagebox.showerror("Σφάλμα", "Μη έγκυρη ημερομηνία. Χρησιμοποιήστε μορφή YYYY-MM-DD.")
            return

        loc = self.e_loc.get().strip()
        if not loc:
            messagebox.showerror("Σφάλμα", "Η τοποθεσία δεν μπορεί να είναι κενή.")
            return

        amt_str = self.e_amt.get().strip()
        try:
            amt = float(amt_str)
            if amt <= 0:
                messagebox.showerror("Σφάλμα", "Το απαιτούμενο ποσό πρέπει να είναι θετικός αριθμός.")
                return
        except ValueError:
            messagebox.showerror("Σφάλμα", "Το απαιτούμενο ποσό πρέπει να είναι έγκυρος αριθμός.")
            return

        try:
            form = SocialActionForm(desc, dt, loc, amt)
            SocialAction.create_action(self._current_user, self._selected_report, form)
            messagebox.showinfo("Επιτυχία",
                                f"Δημιουργήθηκε επιτυχώς!\nΥπόλοιπο pool: {self._pool._total_amount:.2f}€")
        except Exception as ex:
            messagebox.showerror("Σφάλμα", str(ex))
        finally:
            self.build_main_menu()