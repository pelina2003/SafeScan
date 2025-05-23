# -------------------------------------
# EMYConnector: Συνδέεται με την ΕΜΥ
# -------------------------------------
class EMYConnector:
    def fetch_data(self):
        # Προσομοίωση λήψης δεδομένων από την ΕΜΥ
        print("Fetching weather data from EMY...")
        return {
            "temperature": 43,
            "precipitation": "heavy",
            "wind": 90
        }

# -------------------------------------
# AnalyzeResult: Αποτέλεσμα ανάλυσης καιρού
# -------------------------------------
class AnalyzeResult:
    def __init__(self):
        self.warnings = []

    def add_warning(self, title, description):
        self.warnings.append({
            "title": title,
            "description": description
        })

    def contains_extreme_weather(self):
        return len(self.warnings) > 0

    def get_warnings(self):
        return self.warnings

# -------------------------------------
# Analyzer: Αναλύει τα δεδομένα καιρού
# -------------------------------------
class Analyzer:
    def analyze(self, weather_data):
        print("Analyzing weather data...")
        result = AnalyzeResult()

        if weather_data["temperature"] > 40:
            result.add_warning("Heatwave", "High temperature detected")

        if weather_data["precipitation"] == "heavy":
            result.add_warning("Heavy Rain", "Risk of flooding")

        if weather_data["wind"] > 80:
            result.add_warning("Storm", "Strong winds detected")

        return result

# -------------------------------------
# NotificationSender: Στέλνει ειδοποιήσεις
# -------------------------------------
class NotificationSender:
    def send_notifications(self, warnings):
        for warning in warnings:
            print(f"🔔 Notification: {warning['title']} - {warning['description']}")

# -------------------------------------
# DatabaseManager: Αποθηκεύει τις προειδοποιήσεις
# -------------------------------------
class DatabaseManager:
    def save_analysis(self, analysis_result):
        print("Saving warnings to database...")
        for warning in analysis_result.get_warnings():
            print(f"💾 Saved: {warning['title']} - {warning['description']}")

# -------------------------------------
# WeatherController: Ο ελεγκτής του συστήματος
# -------------------------------------
class WeatherController:
    def __init__(self, emy_connector, analyzer, notifier, database_manager):
        self.emy_connector = emy_connector
        self.analyzer = analyzer
        self.notifier = notifier
        self.database_manager = database_manager

    def update_weather_data(self):
        raw_data = self.emy_connector.fetch_data()
        analysis_result = self.analyzer.analyze(raw_data)
        self.database_manager.save_analysis(analysis_result)

        if analysis_result.contains_extreme_weather():
            self.notifier.send_notifications(analysis_result.get_warnings())
        else:
            print("✅ Ο καιρός είναι ήπιος στην περιοχή σας.")

# -------------------------------------
# Κύριο πρόγραμμα
# -------------------------------------
if __name__ == "__main__":
    controller = WeatherController(
        emy_connector=EMYConnector(),
        analyzer=Analyzer(),
        notifier=NotificationSender(),
        database_manager=DatabaseManager()
    )
    controller.update_weather_data()
