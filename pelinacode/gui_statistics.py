import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from dataclasses import dataclass
from typing import List

# === Οντότητες ===

@dataclass
class DateRange:
    start: str
    end: str

@dataclass
class StatisticalData:
    category: str
    region: str
    dateRange: DateRange
    count: int

    def getCount(self) -> int:
        return self.count

@dataclass
class FilterSelection:
    category: str
    type: str
    format: str
    region: str
    dateRange: DateRange

# === Chart ===

class Chart:
    def __init__(self, chart_type: str, chart_format: str, data: List[StatisticalData]):
        self.type = chart_type
        self.format = chart_format
        self.data = data

    def render(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = [d.dateRange.start for d in self.data]
        values = [d.getCount() for d in self.data]
        if self.type == "bar":
            ax.bar(labels, values, color='skyblue')
            ax.set_xlabel("Έτος ή Μήνας")
            ax.set_ylabel("Αριθμός Αναφορών")
            ax.yaxis.get_major_locator().set_params(integer=True)
        elif self.type == "pie":
            ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title("Στατιστικά Αναφορών")
        return fig

    def export(self, path):
        fig = self.render()
        fig.savefig(path)

# === Boundary ===

class StatisticsDisplay:
    def __init__(self, root):
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

# === Controller ===

class StatisticsController:
    def __init__(self, display, db_name="safescan.db"):
        self.display = display
        self.db_name = db_name

    def checkData(self, selection: FilterSelection):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM confirmed_reports
            WHERE category = ? AND region = ? AND date LIKE ? AND status = 'confirmed'
        """, (selection.category, selection.region, f"{selection.dateRange.start}%"))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def generateChart(self, selection: FilterSelection):
        data = self.fetchData(selection)
        if not data:
            self.display.displayError("Δεν βρέθηκαν διαθέσιμα δεδομένα για τα επιλεγμένα φίλτρα. Παρακαλώ τροποποιήστε τις επιλογές σας.")
            return None
        return Chart(selection.type, selection.format, data)

    def fetchData(self, selection: FilterSelection):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, COUNT(*) FROM confirmed_reports
            WHERE category = ? AND region = ? AND date LIKE ? AND status = 'confirmed'
            GROUP BY date
            ORDER BY date
        """, (selection.category, selection.region, f"{selection.dateRange.start}%"))
        rows = cursor.fetchall()
        conn.close()
        return [StatisticalData(selection.category, selection.region, DateRange(date, date), count)
                for date, count in rows]

# === Φόρμα ===

class StatFilterForm:
    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = tk.Frame(parent)
        self.frame.pack()

        self.category_var = tk.StringVar()
        self.chart_type_var = tk.StringVar()
        self.region_var = tk.StringVar()

        tk.Label(self.frame, text="Κατηγορία").pack()
        ttk.Combobox(self.frame, textvariable=self.category_var,
                     values=["Πυρκαγιά", "Πλημμύρα", "Φυσική καταστροφή", "Κοινωνικά Ζητήματα"]).pack()

        tk.Label(self.frame, text="Τύπος Διαγράμματος").pack()
        ttk.Combobox(self.frame, textvariable=self.chart_type_var,
                     values=["bar", "pie"]).pack()

        tk.Label(self.frame, text="Περιοχή").pack()
        tk.Entry(self.frame, textvariable=self.region_var).pack()

        tk.Button(self.frame, text="Υποβολή", command=self.submitFilters).pack(pady=10)

    def submitFilters(self):
        selection = FilterSelection(
            category=self.category_var.get(),
            type=self.chart_type_var.get(),
            format="png",
            region=self.region_var.get(),
            dateRange=DateRange("2023", "2023")
        )
        if self.controller.checkData(selection):
            chart = self.controller.generateChart(selection)
            if chart:
                self.controller.display.displayChart(chart)
        else:
            self.controller.display.displayError("Δεν βρέθηκαν διαθέσιμα δεδομένα για τα επιλεγμένα φίλτρα. Παρακαλώ τροποποιήστε τις επιλογές σας.")

# === Εκκίνηση GUI ===

def start_statistics_gui():
    root = tk.Tk()
    root.title("Στατιστικά Αναφορών")
    root.geometry("650x600")

    display = StatisticsDisplay(root)
    controller = StatisticsController(display)
    form = StatFilterForm(root, controller)

    root.mainloop()

if __name__ == "__main__":
    start_statistics_gui()
