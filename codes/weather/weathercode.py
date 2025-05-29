from typing import List


# -------------------------------
# Κλάση User
class User:
    def __init__(self, username: str, location: str):
        self.username = username
        self.location = location

    def getLocation(self) -> str:
        return self.location

    def notify(self, message: str):
        print(f"🔔 [{self.username}] Ειδοποίηση: {message}")


# -------------------------------
# Κλάση WeatherEvent
class WeatherEvent:
    def __init__(self, event_type: str, location: str):
        self.event_type = event_type
        self.location = location

    def getLocation(self) -> str:
        return self.location

    def getType(self) -> str:
        return self.event_type


# -------------------------------
# Κλάση RiskAssessment
class RiskAssessment:
    def __init__(self):
        self.risk_percentage = 0.0

    def assessRisk(self, event: WeatherEvent):
        event_type = event.getType()
        if event_type == "heatwave":
            self.risk_percentage = 85.0
        elif event_type == "storm":
            self.risk_percentage = 60.0
        elif event_type == "rain":
            self.risk_percentage = 30.0
        else:
            self.risk_percentage = 10.0

    def getRiskPercentage(self) -> float:
        return self.risk_percentage


# -------------------------------
# Κλάση Warning
class Warning:
    def __init__(self, event: WeatherEvent, risk: RiskAssessment):
        self.event = event
        self.risk = risk

    def getWarningText(self) -> str:
        return f"{self.event.getType().upper()} στην {self.event.getLocation()} - Κίνδυνος: {self.risk.getRiskPercentage()}%"


# -------------------------------
# Κλάση ProtectionAdvice
class ProtectionAdvice:
    def __init__(self):
        self.advice_text = ""

    def generateAdvice(self, event: WeatherEvent):
        event_type = event.getType()
        if event_type == "heatwave":
            self.advice_text = "Αποφύγετε την έκθεση στον ήλιο."
        elif event_type == "storm":
            self.advice_text = "Μείνετε σε ασφαλές μέρος."
        elif event_type == "rain":
            self.advice_text = "Οδηγείτε με προσοχή σε βροχή."
        else:
            self.advice_text = "Καμία ειδική οδηγία."

    def getAdviceText(self) -> str:
        return self.advice_text


# -------------------------------
# Κλάση Database
class Database:
    def __init__(self):
        self.saved_events: List[WeatherEvent] = []

    def storeEvent(self, event: WeatherEvent):
        print(f"💾 Αποθηκεύτηκε: {event.getType()} στην {event.getLocation()}")
        self.saved_events.append(event)


# -------------------------------
# Κλάση WeatherForecastPage
class WeatherForecastPage:
    def showForecast(self, warnings: List[Warning]):
        if not warnings:
            print("✅ Ο καιρός τις επόμενες μέρες θα είναι ήπιος στην περιοχή σας.")
        else:
            print("⚠️ Προβλεπόμενα φαινόμενα:")
            for warning in warnings:
                print(f"- {warning.getWarningText()}")


# -------------------------------
# Κλάση WeatherService
class WeatherService:
    def __init__(self, database: Database):
        self.database = database

    def getWeatherData(self) -> List[WeatherEvent]:
        # Προσομοίωση ανάκτησης δεδομένων από ΕΜΥ
        return [
            WeatherEvent("heatwave", "Athens"),
            WeatherEvent("rain", "Patras")
        ]


# -------------------------------
# Εκτέλεση Use Case
user = User("Giannis", "Athens")
database = Database()
service = WeatherService(database)
forecast_page = WeatherForecastPage()

weather_data = service.getWeatherData()
warnings: List[Warning] = []

for event in weather_data:
    risk = RiskAssessment()
    risk.assessRisk(event)
    database.storeEvent(event)

    if user.getLocation() == event.getLocation() and risk.getRiskPercentage() >= 35:
        warning = Warning(event, risk)
        user.notify(warning.getWarningText())

        advice = ProtectionAdvice()
        advice.generateAdvice(event)
        print(f"ℹ️ Συμβουλή: {advice.getAdviceText()}")

        warnings.append(warning)

forecast_page.showForecast(warnings)
