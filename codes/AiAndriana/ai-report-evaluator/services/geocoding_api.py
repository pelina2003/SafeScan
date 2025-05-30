# services/geocoding_api.py

from models.report import Coordinates

class GeocodingAPI:
    def __init__(self):
        # Μπορεί αργότερα να συνδεθεί με πραγματική υπηρεσία (π.χ. Google Maps)
        self.location_map = {
            "Αθήνα": Coordinates(37.9838, 23.7275),
            "Θεσσαλονίκη": Coordinates(40.6401, 22.9444),
            "Πάτρα": Coordinates(38.2466, 21.7346),
            "Ηράκλειο": Coordinates(35.3387, 25.1442),
            "Λάρισα": Coordinates(39.6390, 22.4191)
        }

    def getCoordinates(self, location_name: str) -> Coordinates:
        # Αν βρει αντιστοιχία, επιστρέφει συντεταγμένες
        if location_name in self.location_map:
            coords = self.location_map[location_name]
            print(f"📍 Τοποθεσία \"{location_name}\" → ({coords.latitude}, {coords.longitude})")
            return coords
        else:
            print(f"⚠️ Άγνωστη τοποθεσία \"{location_name}\", επιστροφή default (0.0, 0.0)")
            return Coordinates(0.0, 0.0)
