import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

# Κλάσεις του domain model
class SocialAction:
    def __init__(self, actionId: int, title: str, category: str, location: str):
        self.actionId = actionId
        self.title = title
        self.category = category
        self.location = location

    def getTitle(self) -> str:
        return self.title

class EnvironmentalOrganization:
    def __init__(self, orgId: int, name: str, category: str):
        self.orgId = orgId
        self.name = name
        self.category = category

    def getName(self) -> str:
        return self.name

class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

    def getName(self) -> str:
        return self.name

# === Δημιουργία ή σύνδεση με τη βάση δεδομένων ===

def setup_database():
    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS social_actions (
            actionId INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT,
            location TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS environmental_organizations (
            orgId INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            donationId INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            paymentMethod TEXT NOT NULL,
            userName TEXT NOT NULL,
            date TEXT NOT NULL,
            socialActionId INTEGER,
            environmentalOrgId INTEGER,
            FOREIGN KEY(socialActionId) REFERENCES social_actions(actionId),
            FOREIGN KEY(environmentalOrgId) REFERENCES environmental_organizations(orgId)
        )
    """)

    # Εισαγωγή δειγμάτων αν η βάση είναι κενή
    cursor.execute("SELECT COUNT(*) FROM social_actions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO social_actions (actionId, title, category, location)
            VALUES (?, ?, ?, ?)
        """, [
            (1, "Αναδάσωση στην πλαγιά της Πεντέλης", "Αναδάσωση", "Αττική"),
            (2, "Συλλογή απορριμμάτων στην παραλία Νέας Μάκρης", "Καθαριότητα", "Αττική")
        ])

    cursor.execute("SELECT COUNT(*) FROM environmental_organizations")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO environmental_organizations (orgId, name, category)
            VALUES (?, ?, ?)
        """, [
            (1, "Οργανισμός προστασίας θαλάσσιας χελώνας", "Θάλασσα"),
            (2, "Εταιρεία αναδάσωσης Ελλάδας", "Δάση")
        ])

    conn.commit()
    conn.close()

# === Ανάκτηση διαθέσιμων επιλογών δωρεάς ===

def get_donation_options() -> List[Tuple[str, int, str]]:
    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()
    options = []

    cursor.execute("SELECT actionId, title FROM social_actions")
    for row in cursor.fetchall():
        options.append(("action", row[0], row[1]))

    cursor.execute("SELECT orgId, name FROM environmental_organizations")
    for row in cursor.fetchall():
        options.append(("organization", row[0], row[1]))

    conn.close()
    return options

# === Αποθήκευση δωρεάς ===

def save_donation(amount: float, status: str, payment_method: str,
                  user: User, socialActionId: Optional[int] = None, environmentalOrgId: Optional[int] = None):
    conn = sqlite3.connect("donations.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO donations (
            amount, status, paymentMethod, userName, date, socialActionId, environmentalOrgId
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        amount,
        status,
        payment_method,
        user.getName(),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        socialActionId if socialActionId is not None else None,
        environmentalOrgId if environmentalOrgId is not None else None
    ))

    conn.commit()
    conn.close()

