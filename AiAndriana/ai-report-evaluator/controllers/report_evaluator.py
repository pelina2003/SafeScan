from database.mock_data import get_unverified_reports
from services.image_analysis import analyze_images
from services.text_analysis import analyze_text
from models.ai_models import estimate_risk
from services.geocoding_api import GeocodingAPI
from utils.logger import log_report_evaluation
from controllers.nearby_notifier import notify_nearby_users
from controllers.authority_notifier import notify_authority


def evaluate_reports():
    reports = get_unverified_reports()
    geocoder = GeocodingAPI()

    for report in reports:
        print(f"\n🔍 Επεξεργασία Αναφοράς #{report.id} ({report.location_name})")

        try:
            # 1. Μετατροπή τοποθεσίας σε συντεταγμένες
            report.resolveCoordinates(geocoder)

            # 2. Ανάλυση εικόνας
            image_result = analyze_images(report.images)
            if not image_result.relevant:
                reason = image_result.summary 
                print(f"❌ Απόρριψη: εικόνα ακατάλληλη ({reason})")
                report.updateStatus("INVALID")
                log_report_evaluation(report.id, status='Μη-Έγκυρη', reason=reason)
                continue

            # 3. Ανάλυση κειμένου
            text_result = analyze_text(report.text)
            if not text_result.relevant:
                print("❌ Απόρριψη: περιγραφή ασαφής ή άσχετη")
                report.updateStatus("INVALID")
                log_report_evaluation(report.id, status='Μη-Έγκυρη', reason='Μη αποδεκτή περιγραφή')
                continue

            # 4. Υπολογισμός κινδύνου
            risk, category = estimate_risk(report, text_result=text_result)
            report.updateStatus("VALID", riskScore=risk, riskCategory=category)
            log_report_evaluation(report.id, status='Έγκυρη', risk=risk, category=category)

            # Ειδοποίηση κοντινών χρηστών αν ο κίνδυνος είναι σημαντικός
            if risk >= 60:
                notify_nearby_users(report)

            # Ειδοποίηση αρχών αν ο κίνδυνος είναι υψηλός
            if risk >= 70:
                notify_authority(report)
                
        except Exception as e:
            print(f"⚠️ Σφάλμα κατά την αξιολόγηση: {e}")
            report.updateStatus("PENDING")
            log_report_evaluation(report.id, status='Αξιολόγηση σε εκκρεμότητα', reason=str(e))
