import tkinter as tk
from tkinter import messagebox
from enum import Enum
from datetime import datetime
from typing import List, Optional

# Enum για την κατάσταση δωρεάς
class Status(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"

# Κλάση Χρήστη
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        self.donations: List['Donation'] = []

    def getName(self) -> str:
        return self.name

    def getEmail(self) -> str:
        return self.email

    def addDonation(self, donation: 'Donation'):
        self.donations.append(donation)

    def getDonations(self) -> List['Donation']:
        return self.donations

# Κλάση Συστήματος Πληρωμής
class PaymentSystem:
    def __init__(self, name: str, maxAmount: float):
        self.name = name
        self.maxAmount = maxAmount

    def validateAmount(self, amount: float) -> bool:
        return 0 < amount <= self.maxAmount

    def getName(self) -> str:
        return self.name

# Κλάση Κοινωνικής Δράσης
class SocialAction:
    def __init__(self, actionId: int, title: str, category: str, location: str):
        self.actionId = actionId
        self.title = title
        self.category = category
        self.location = location

    def getTitle(self) -> str:
        return self.title

    def getCategory(self) -> str:
        return self.category

    def getLocation(self) -> str:
        return self.location

# Κλάση Περιβαλλοντικού Οργανισμού
class EnvironmentalOrganization:
    def __init__(self, orgId: int, name: str, category: str):
        self.orgId = orgId
        self.name = name
        self.category = category

    def getName(self) -> str:
        return self.name

    def getCategory(self) -> str:
        return self.category

# Κλάση Δωρεάς
class Donation:
    def __init__(self, donationId: int, amount: float, date: datetime,
                 paymentMethod: str, user: User,
                 socialAction: Optional[SocialAction] = None,
                 environmentalOrganization: Optional[EnvironmentalOrganization] = None):
        self.donationId = donationId
        self.amount = amount
        self.date = date
        self.paymentMethod = paymentMethod
        self.status = Status.PENDING
        self.user = user
        self.socialAction = socialAction
        self.environmentalOrganization = environmentalOrganization
        user.addDonation(self)

    def confirmDonation(self):
        self.status = Status.CONFIRMED

    def failDonation(self):
        self.status = Status.FAILED

    def getStatus(self) -> Status:
        return self.status

# ---------------------------------------------------
# GUI ΜΕΡΟΣ
# ---------------------------------------------------

user = User(1, "user1", "user1@example.com")
paymentSystem = PaymentSystem("Credit Card", 1000.0)
options = [
    SocialAction(1, "Αναδάσωση στην πλαγιά της Πεντέλης", "Αναδάσωση", "Πεντέλη"),
    SocialAction(2, "Συλλογή απορριμμάτων στην παραλία Νέας Μάκρης", "Καθαρισμός", "Νέα Μάκρη"),
    EnvironmentalOrganization(1, "Οργανισμός προστασίας θαλάσσιας χελώνας", "Θάλασσα")
]

selected_option = None

def select_option(index: int):
    global selected_option
    selected_option = options[index]
    open_donation_window()

def open_donation_window():
    window.destroy()

    donation_window = tk.Tk()
    donation_window.title("Δωρεά")

    tk.Label(donation_window, text="Εισαγάγετε το ποσό της δωρεάς", font=("Arial", 14)).pack(pady=10)
    amount_entry = tk.Entry(donation_window, width=20, font=("Arial", 12))
    amount_entry.pack(pady=5)

    # Προβολή στόχου
    if isinstance(selected_option, SocialAction):
        target_text = selected_option.getTitle()
    elif isinstance(selected_option, EnvironmentalOrganization):
        target_text = selected_option.getName()
    else:
        target_text = "Άγνωστη επιλογή"

    tk.Label(donation_window, text="Επιλεγμένη Δράση / Οργανισμός:", font=("Arial", 10)).pack(pady=5)
    tk.Label(donation_window, text=target_text, font=("Arial", 10, "bold")).pack(pady=5)

    def confirm_donation():
        try:
            amount = float(amount_entry.get())
            if not paymentSystem.validateAmount(amount):
                raise ValueError
            donation = Donation(
                donationId=len(user.getDonations()) + 1,
                amount=amount,
                date=datetime.now(),
                paymentMethod=paymentSystem.getName(),
                user=user,
                socialAction=selected_option if isinstance(selected_option, SocialAction) else None,
                environmentalOrganization=selected_option if isinstance(selected_option, EnvironmentalOrganization) else None
            )
            donation.confirmDonation()
            messagebox.showinfo("Επιτυχία", f"✅ Επιβεβαιώθηκε δωρεά {amount}€ για: {target_text}")
            donation_window.destroy()
        except ValueError:
            messagebox.showerror("Σφάλμα", "❌ Το ποσό δεν είναι έγκυρο. Επιλέξτε ποσό μεταξύ 0 και 1000€.")

    def cancel_donation():
        messagebox.showinfo("Ακύρωση", "Η δωρεά ακυρώθηκε.")
        donation_window.destroy()

    button_frame = tk.Frame(donation_window)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Επιβεβαίωση", command=confirm_donation, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Ακύρωση", command=cancel_donation, font=("Arial", 12)).pack(side=tk.RIGHT, padx=10)

    donation_window.mainloop()

# Κύριο παράθυρο επιλογής δράσης/οργανισμού
window = tk.Tk()
window.title("Επιλογή Δράσης/Οργανισμού")

tk.Label(window, text="Επιλέξτε μια δράση ή οργανισμό για δωρεά", font=("Arial", 14)).pack(pady=10)

for i, option in enumerate(options):
    text = option.getTitle() if isinstance(option, SocialAction) else option.getName()
    tk.Button(window, text=text, width=50, command=lambda idx=i: select_option(idx), font=("Arial", 12)).pack(pady=5)

window.mainloop()

