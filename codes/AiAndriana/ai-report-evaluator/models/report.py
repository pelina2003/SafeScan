# models/report.py

class Coordinates:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude


class Report:
    def __init__(self, id: int, images: list, text: str, location_name: str):
        self.id = id
        self.images = images
        self.text = text
        self.location_name = location_name  # ← προστέθηκε
        self.coordinates = None             # ← γεμίζει αργότερα
        self.status = "PENDING"
        self.riskScore = None
        self.riskCategory = None

    def isValid(self):
        return self.status == "VALID"

    def updateStatus(self, newStatus: str, riskScore=None, riskCategory=None):
        self.status = newStatus
        if riskScore is not None:
            self.riskScore = riskScore
        if riskCategory is not None:
            self.riskCategory = riskCategory
        print(f"[Αναφορά {self.id}] → Κατάσταση: {self.status}, "
              f"Κίνδυνος: {self.riskScore}, Κατηγορία: {self.riskCategory}")

    def resolveCoordinates(self, geocoding_api):
        """Καλεί το Geocoding API για να μετατρέψει την τοποθεσία σε συντεταγμένες."""
        self.coordinates = geocoding_api.getCoordinates(self.location_name)
