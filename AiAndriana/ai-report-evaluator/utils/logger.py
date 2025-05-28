from datetime import datetime

def log_report_evaluation(report_id, status, reason=None, risk=None, category=None):
    with open("log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] Αναφορά {report_id}: Κατάσταση={status}"
        if reason:
            line += f", Λόγος={reason}"
        if risk is not None and category:
            line += f", Κίνδυνος={risk}%, Κατηγορία={category}"
        f.write(line + "\n")
