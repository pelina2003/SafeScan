from database.mock_users import get_active_users
from services.notification_manager import calculate_distance

def notify_nearby_users(report):
    radius_km = 2  # ή 0.5 για μικρότερη ακτίνα
    eligible_users = []

    for user in get_active_users():
        if not user.location_enabled:
            print(f"⛔ Χρήστης {user.name} έχει απενεργοποιημένο GPS.")
            continue
        if not user.coordinates:
            print(f"❓ Δεν υπάρχουν συντεταγμένες για τον χρήστη {user.name}.")
            continue
        distance = calculate_distance(report.coordinates, user.coordinates)
        if distance <= radius_km and user.push_enabled:
            eligible_users.append((user, distance))
        else:
            print(f"🔕 Χρήστης {user.name} εκτός ακτίνας ή δεν δέχεται ειδοποιήσεις.")

    if not eligible_users:
        print("📭 Κανένας χρήστης εντός ακτίνας.")
        return

    for user, dist in eligible_users:
        print(f"📲 Ειδοποίηση στον {user.name} | Απόσταση: {dist*1000:.0f}m | "
              f"Περιγραφή: {report.text}")

        # TODO: Υλοποίηση πραγματικής αποστολής push notification
        # push_notification_service.send(user.device_token, message)

    print(f"✅ Εστάλησαν {len(eligible_users)} ειδοποιήσεις σε κοντινούς χρήστες.")
