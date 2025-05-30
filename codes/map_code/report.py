# report.py
class Report:
    def __init__(self, report_id, report_type, latitude, longitude, status):
        self.id = report_id
        self.type = report_type
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
