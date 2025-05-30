import tkinter as tk
from tkinter import messagebox
from typing import List


class User:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location

    def getLocation(self) -> str:
        return self.location

    def notify(self, message: str):
        messagebox.showinfo(f"Ειδοποίηση για {self.username}", message)


class WeatherEvent:
    def __init__(self, event_type: str, location: str):
        self.event_type = event_type
        self.location = location

    def getLocation(self) -> str:
        return self.location

    def getType(self) -> str:
        return self.event_type


class RiskAssessment:
    def __init__(self):
        self.risk_percentage = 0.0

    def assessRisk(self, event: WeatherEvent):
        if event.getType() == "heatwave":
            self.risk_percentage = 85.0
        elif event.getType() == "storm":
            self.risk_percentage = 65.0
        elif event.getType() == "rain":
            self.risk_percentage = 40.0
        else:
            self.risk_percentage = 10.0

    def getRiskPercentage(self) -> float:
        return self.risk_percentage


class Warning:
    def __init__(self, event: WeatherEvent, risk: RiskAssessment):
        self.event = event
        self.risk = risk

    def getWarningText(self) -> str:
        return f"{self.event.getType().upper()} στην {self.event.getLocation()} - Κίνδυνος: {self.risk.getRiskPercentage()}%"


class ProtectionAdvice:
    def __init__(self):
        self.advice_text = ""

    def generateAdvice(self, event: WeatherEvent):
        if event.getType() == "heatwave":
            self.advice_text = "Αποφύγετε την έκθεση στον ήλιο."
        elif event.getType() == "storm":
            self.advice_text = "Μείνετε σε ασφαλές μέρος."
        elif event.getType() == "rain":
            self.advice_text = "Προσέχετε σε περιοχές με ολισθηρότητα."
        else:
            self.advice_text = "Καμία ειδική οδηγία."

    def getAdviceText(self) -> str:
        return self.advice_text


class Database:
    def __init__(self):
        self.saved_events: List[WeatherEvent] = []

    def storeEvent(self, event: WeatherEvent):
        self.saved_events.append(event)


class WeatherForecastPage:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def showForecast(self, warnings: List[Warning]):
        self.text_widget.delete("1.0", tk.END)
        if not warnings:
            self.text_widget.insert(tk.END, "✅ Ο καιρός τις επόμενες μέρες θα είναι ήπιος στην περιοχή σας.\n")
        else:
            self.text_widget.insert(tk.END, "⚠️ Προβλεπόμενα φαινόμενα:\n")
            for warning in warnings:
                self.text_widget.insert(tk.END, f"- {warning.getWarningText()}\n")


class WeatherService:
    def __init__(self, database: Database):
        self.database = database

    def getWeatherData(self) -> List[WeatherEvent]:
        return [
            WeatherEvent("heatwave", "Athens"),
            WeatherEvent("rain", "Thessaloniki"),
            WeatherEvent("storm", "Patras")
        ]


class WeatherController:
    def __init__(self, root):
        self.database = Database()
        self.service = WeatherService(self.database)
        self.user = User("andriana", "Athens")

        self.root = root
        self.root.title("Έλεγχος Καιρού")
        self.root.geometry("600x400")
        self.root.configure(bg="lightblue")

        self.result_text = tk.Text(root, height=10, width=70, font=("Arial", 12))
        self.result_text.pack(pady=10)

        self.forecast_page = WeatherForecastPage(self.result_text)

        self.button = tk.Button(
            root, text="Έλεγχος Καιρού",
            command=self.updateWeatherPage,
            font=("Arial", 14), bg="white"
        )
        self.button.pack(pady=10)

    def getWeatherForecast(self) -> List[WeatherEvent]:
        return self.service.getWeatherData()

    def assessRisk(self, event: WeatherEvent) -> RiskAssessment:
        risk = RiskAssessment()
        risk.assessRisk(event)
        return risk

    def notifyUsers(self, warning: Warning, event: WeatherEvent):
        self.user.notify(warning.getWarningText())
        advice = ProtectionAdvice()
        advice.generateAdvice(event)
        messagebox.showinfo("Συμβουλή Προστασίας", advice.getAdviceText())

    def updateWeatherPage(self):
        warnings: List[Warning] = []

        for event in self.getWeatherForecast():
            risk = self.assessRisk(event)
            self.database.storeEvent(event)

            if event.getLocation() == self.user.getLocation() and risk.getRiskPercentage() > 35:
                warning = Warning(event, risk)
                self.notifyUsers(warning, event)
                warnings.append(warning)

        self.forecast_page.showForecast(warnings)


if __name__ == "__main__":
    root = tk.Tk()
    controller = WeatherController(root)
    root.mainloop()