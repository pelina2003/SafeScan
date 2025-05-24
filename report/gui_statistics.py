import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

# === Entity ===
class StatQuery:
    def __init__(self, category, chart_type, region, time_range):
        self.category = category
        self.chart_type = chart_type
        self.region = region
        self.time_range = time_range

    def getQueryParameters(self):
        return {
            "category": self.category,
            "chart_type": self.chart_type,
            "region": self.region,
            "time_range": self.time_range
        }

# === Boundary ===
class StatFilterForm:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = tk.Frame(parent)
        self.frame.pack()

        self.category_var = tk.StringVar()
        self.chart_type_var = tk.StringVar()
        self.region_var = tk.StringVar()
        self.time_range_var = tk.StringVar()

        tk.Label(self.frame, text="Κατηγορία").pack()
        ttk.Combobox(self.frame, textvariable=self.category_var, values=["Εγκληματικότητα", "Φυσικές Καταστροφές", "Πυρκαγιές", "Κοινωνικά Ζητήματα"]).pack()

        tk.Label(self.frame, text="Τύπος Διαγράμματος").pack()
        ttk.Combobox(self.frame, textvariable=self.chart_type_var, values=["bar", "pie"]).pack()

        tk.Label(self.frame, text="Περιοχή").pack()
        tk.Entry(self.frame, textvariable=self.region_var).pack()

        tk.Label(self.frame, text="Χρονικό Διάστημα").pack()
        tk.Entry(self.frame, textvariable=self.time_range_var).pack()

        tk.Button(self.frame, text="Υποβολή", command=self.submitFilters).pack(pady=10)

    def submitFilters(self):
        query = StatQuery(
            self.category_var.get(),
            self.chart_type_var.get(),
            self.region_var.get(),
            self.time_range_var.get()
        )
        self.controller.handleQuery(query)

# === Entity ===
class Chart:
    def __init__(self, title, chart_type, data):
        self.title = title
        self.chart_type = chart_type
        self.data = data

    def render(self):
        fig, ax = plt.subplots(figsize=(5, 4))
        if self.chart_type == "bar":
            ax.bar(self.data.keys(), self.data.values())
        elif self.chart_type == "pie":
            ax.pie(self.data.values(), labels=self.data.keys(), autopct='%1.1f%%')
        ax.set_title(self.title)
        return fig

    def export(self, path):
        fig = self.render()
        fig.savefig(path)

# === Control ===
class StatisticsController:
    def __init__(self, display):
        self.display = display

    def handleQuery(self, query):
        data = self.fetchData(query)
        if not data:
            self.display.displayError("Δεν βρέθηκαν διαθέσιμα δεδομένα για τα επιλεγμένα φίλτρα.")
            return
        chart = self.generateChart(data, query)
        self.display.displayChart(chart)

    def fetchData(self, query):
        # Dummy implementation for simulation
        # In real scenario, filter DB using query.getQueryParameters()
        if query.category == "Πυρκαγιές" and query.region.lower() == "πάτρα":
            return {}  # Simulate no data
        return {"Ιανουάριος": 3, "Φεβρουάριος": 6, "Μάρτιος": 2}

    def generateChart(self, data, query):
        return Chart(f"{query.category} - {query.region}", query.chart_type, data)

# === Boundary ===
class StatisticsDisplay:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

    def displayChart(self, chart):
        for widget in self.frame.winfo_children():
            widget.destroy()
        fig = chart.render()
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def displayError(self, message):
        messagebox.showwarning("Καμία καταγραφή", message)

# === Εκκίνηση Εφαρμογής ===
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Στατιστικά Αναφορών")
    root.geometry("600x600")

    display = StatisticsDisplay(root)
    controller = StatisticsController(display)
    form = StatFilterForm(root, controller)

    root.mainloop()
