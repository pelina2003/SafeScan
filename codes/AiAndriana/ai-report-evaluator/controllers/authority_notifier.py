import requests
from database.mock_authorities import get_authorities

def notify_authority(report):
    if report.riskScore is None or report.riskScore < 70:
        print("ℹ️ Το ποσοστό κινδύνου είναι κάτω από το όριο ειδοποίησης αρχών.")
        return

    category = report.riskCategory
    authorities = get_authorities()
    target = next((a for a in authorities if a.category == category), None)

    if not target:
        target = next((a for a in authorities if a.category == "default"), None)
        print(f"⚠️ Δεν βρέθηκε ειδική αρχή για την κατηγορία '{category}', χρήση {target.name}")

    data = {
        "description": report.text,
        "location": report.location_name,
        "risk": report.riskScore,
        "category": report.riskCategory
    }

    success = False
    for attempt in range(1, 3):  # 2 προσπάθειες
        try:
            print(f"📡 Προσπάθεια {attempt}: Αποστολή στην {target.name}...")
            response = requests.post(target.api_url, json=data, timeout=5)

            if response.status_code == 200:
                print(f"✅ Η {target.name} απάντησε επιτυχώς.")
                success = True
                break
            else:
                print(f"❌ Απόρριψη από {target.name} (status {response.status_code})")

        except Exception as e:
            print(f"🚨 Σφάλμα αποστολής ({target.name}): {e}")

    if not success:
        print("🛑 Αποτυχία μετά από 2 προσπάθειες. Ενημερώνεται ο διαχειριστής.")
        # log_to_admin_alerts(report.id, target.name, data)
