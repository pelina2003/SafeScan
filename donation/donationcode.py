from typing import List, Optional
from datetime import datetime

# ----------------------------
# Κλάση Χρήστη
class User:
    def __init__(self, user_id: int, username: str, email: str):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__donations: List[Donation] = []

    def get_username(self) -> str:
        return self.__username

    def add_donation(self, donation: 'Donation'):
        self.__donations.append(donation)

    def get_donations(self) -> List['Donation']:
        return self.__donations

# ----------------------------
# Κλάση Κοινωνικής Δράσης
class SocialAction:
    def __init__(self, action_id: int, title: str, category: str, location: str):
        self.__action_id = action_id
        self.__title = title
        self.__category = category
        self.__location = location

    def get_title(self) -> str:
        return self.__title

    def get_category(self) -> str:
        return self.__category

    def get_location(self) -> str:
        return self.__location

# ----------------------------
# Κλάση Περιβαλλοντικού Οργανισμού
class EnvironmentalOrganization:
    def __init__(self, org_id: int, name: str, category: str):
        self.__org_id = org_id
        self.__name = name
        self.__category = category

    def get_name(self) -> str:
        return self.__name

    def get_category(self) -> str:
        return self.__category

# ----------------------------
# Κλάση Συστήματος Πληρωμής
class PaymentSystem:
    def __init__(self, name: str, max_amount: float):
        self.__name = name
        self.__max_amount = max_amount

    def validate_amount(self, amount: float) -> bool:
        return 0 < amount <= self.__max_amount

    def get_name(self) -> str:
        return self.__name

# ----------------------------
# Κλάση Δωρεάς
class Donation:
    def __init__(self, amount: float, date: datetime,
                 payment_method: str, user: User,
                 action: Optional[SocialAction] = None,
                 organization: Optional[EnvironmentalOrganization] = None):
        self.__amount = amount
        self.__date = date
        self.__payment_method = payment_method
        self.__user = user
        self.__action = action
        self.__organization = organization
        self.__status = "PENDING"

        user.add_donation(self)

    def confirm(self):
        self.__status = "CONFIRMED"

    def cancel(self):
        self.__status = "CANCELLED"

    def get_summary(self) -> str:
        target = ""
        if self.__action:
            target = self.__action.get_title()
        elif self.__organization:
            target = self.__organization.get_name()
        return (f"Δωρεά {self.__amount}€ από {self.__user.get_username()} "
                f"προς {target} με μέθοδο {self.__payment_method} "
                f"[Κατάσταση: {self.__status}]")


# ----------------------------
# Κύρια Συνάρτηση Χρήστη
def run_donation_use_case():
    # Δημιουργία δεδομένων
    user = User(1, "giannis", "giannis@example.com")
    actions = [
        SocialAction(1, "Καθαρισμός παραλίας", "Εθελοντισμός", "Πάτρα"),
        SocialAction(2, "Διανομή τροφίμων", "Αλληλεγγύη", "Αθήνα")
    ]
    orgs = [
        EnvironmentalOrganization(1, "GreenEarth", "Αναδάσωση"),
        EnvironmentalOrganization(2, "SeaGuardians", "Θάλασσα")
    ]
    payment_system = PaymentSystem("Πιστωτική Κάρτα", 1000.0)

    print("=== ΔΙΑΘΕΣΙΜΕΣ ΔΡΑΣΕΙΣ ===")
    for i, action in enumerate(actions):
        print(f"{i+1}. {action.get_title()} - {action.get_category()} ({action.get_location()})")

    print("=== ΠΕΡΙΒΑΛΛΟΝΤΙΚΟΙ ΟΡΓΑΝΙΣΜΟΙ ===")
    for i, org in enumerate(orgs):
        print(f"{i+1+len(actions)}. {org.get_name()} - {org.get_category()}")

    try:
        selection = int(input("Επιλέξτε αριθμό για δωρεά: "))
    except ValueError:
        print("Μη έγκυρη επιλογή.")
        return

    if 1 <= selection <= len(actions):
        selected = actions[selection - 1]
        target_type = "action"
    elif len(actions) < selection <= len(actions) + len(orgs):
        selected = orgs[selection - len(actions) - 1]
        target_type = "org"
    else:
        print("Μη έγκυρη επιλογή.")
        return

    try:
        amount = float(input("Εισάγετε ποσό δωρεάς (€): "))
    except ValueError:
        print("Μη έγκυρο ποσό.")
        return

    if not payment_system.validate_amount(amount):
        print("❌ Το ποσό δεν είναι έγκυρο.")
        return

    confirm = input("Επιβεβαιώνετε τη δωρεά; (ν/ο): ")
    if confirm.lower() != 'ν':
        print("Η δωρεά ακυρώθηκε.")
        return

    if target_type == "action":
        donation = Donation(amount, datetime.now(), payment_system.get_name(), user, action=selected)
    else:
        donation = Donation(amount, datetime.now(), payment_system.get_name(), user, organization=selected)

    donation.confirm()
    print("✅ Επιτυχής δωρεά!")
    print(donation.get_summary())


# Εκκίνηση προγράμματος
run_donation_use_case()
