# database/mock_data.py

from models.report import Report

def get_unverified_reports():
    return [
        Report(
            id=1,
            images=['static/sample_reports/fire1.jpg'],
            text='Υπάρχει φωτιά κοντά στο δάσος.',
            location_name='Αθήνα'
        ),
        Report(
            id=2,
            images=['static/sample_reports/meme.jpg'],
            text='Απλά μια αστεία εικόνα.',
            location_name='Θεσσαλονίκη'
        )
    ]

def update_report_status(report_id, status, risk=None, category=None):
    print(f"[Αναφορά {report_id}] → Κατάσταση: {status}, Κίνδυνος: {risk}, Κατηγορία: {category}")
