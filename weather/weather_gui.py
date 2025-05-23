import tkinter as tk
from tkinter import messagebox

# ----- EMYConnector -----
class EMYConnector:
    def fetch_data(self):
        print("Fetching weather data from EMY...")
        return {
            "temperature": 43,
            "precipitation": "heavy",
            "wind": 90
        }

# ----- AnalyzeResult -----
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

# ----- Analyzer -----
class Analyzer:
    def analyze(self, weather_data):
        print("Analyzing weather data...")
        result = AnalyzeResult()

        if weather_data["temperature"] > 40:
            result.add_warning("Καύσωνας", "Η θερμοκρασία ξεπέρασε τους 40°C")

        if weather_data["precipitation"] == "heavy":
            result.add_warning("Έντονες Βροχοπτώσεις", "Κίνδυνος πλημμύρας")

        if weather_data["wind"] > 80:
            result.add_warning("Θύελλα", "Ισχυροί άνεμοι εντοπίστηκαν")

        return result

# ----- NotificationSender -----
class NotificationSender:
    def send_notifications(self, warnings):
        messages = []
        for warning in warnings:
            msg = f"{warning['title']} - {warning['description']}"
            print(f"Notification: {msg}")
            messages.append(msg)

        if messages:
            messagebox.showwarning("Καιρική Προειδοποίηση", "\n".join(messages))

        return messages

# ----- DatabaseManager -----
class DatabaseManager:
    def save_analysis(self, analysis_result):
        print("Saving warnings to database...")
        for warning in analysis_result.get_warnings():
            print(f"Saved: {warning['title']} - {warning['description']}")

# ----- WeatherController -----
class WeatherController:
    def __init__(self):
        self.emy_connector = EMYConnector()
        self.analyzer = Analyzer()
        self.notifier = NotificationSender()
        self.database_manager = DatabaseManager()

    def update_weather_data(self):
        raw_data = self.emy_connector.fetch_data()
        analysis_result = self.analyzer.analyze(raw_data)
        self.database_manager.save_analysis(analysis_result)

        if analysis_result.contains_extreme_weather():
            warnings = self.notifier.send_notifications(analysis_result.get_warnings())
            return "\n".join([f"⚠️ {w}" for w in warnings])
        else:
            return "✅ Ο καιρός τις επόμενες μέρες θα είναι ήπιος στην περιοχή σας.\nΘα σας ειδοποιήσουμε για τυχόν αλλαγές."

# ----- GUI -----
class WeatherApp:
    def __init__(self, root):
        self.controller = WeatherController()
        self.root = root
        self.root.title("Έλεγχος Καιρού")
        self.root.geometry("600x400")
        self.root.configure(bg="lightblue")

        self.label = tk.Label(root, text="Καλώς ήρθατε στην Ενημέρωση Καιρού!", font=("Arial", 16), bg="lightblue")
        self.label.pack(pady=20)

        self.button = tk.Button(root, text="Έλεγχος Καιρού", command=self.check_weather, font=("Arial", 14), bg="white")
        self.button.pack(pady=10)

        self.result_text = tk.Text(root, height=10, width=70, font=("Arial", 12))
        self.result_text.pack(pady=10)

    def check_weather(self):
        result = self.controller.update_weather_data()
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result)

# ----- Εκτέλεση εφαρμογής -----
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
