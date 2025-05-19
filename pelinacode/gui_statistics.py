import tkinter as tk 
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

# === Domain ===

class FilterSelection:
    def __init__(self, category, chart_type, region, time_range="2023"):
        self.category = category
        self.chart_type = chart_type
        self.region = region
        self.time_range = time_range

class Chart:
    def __init__(self, title, chart_type, data):
        self.title = title
        self.chart_type = chart_type
        self.data = data

    def render(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        if self.chart_type == "bar":
            ax.bar(self.data.keys(), self.data.values(), color='skyblue')
            ax.set_xlabel("Έτος ή Μήνας")
            ax.set_ylabel("Αριθμός Αναφορών")
            ax.yaxis.get_major_locator().set_params(integer=True)
        elif self.chart_type == "pie":
            ax.pie(self.data.values(), labels=self.data.keys(), autopct='%1.1f%%')
        ax.set_title(self.title)
        return fig

    def export(self, path):
        fig = self.render()
        fig.savefig(path)

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
        """, (selection.category, selection.region, f"{selection.time_range}%"))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def generateChart(self, selection: FilterSelection):
        data = self.fetchData(selection)
        if not data:
            self.display.displayError("Δεν βρέθηκαν διαθέσιμα δεδομένα για τα επιλεγμένα φίλτρα. Παρακαλώ τροποποιήστε τις επιλογές σας.")
            return None
        return Chart(f"{selection.category} - {selection.region}", selection.chart_type, data)

    def fetchData(self, selection: FilterSelection):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, COUNT(*) FROM confirmed_reports
            WHERE category = ? AND region = ? AND date LIKE ? AND status = 'confirmed'
            GROUP BY date
            ORDER BY date
        """, (selection.category, selection.region, f"{selection.time_range}%"))
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows} if rows else {}

# === Φόρμα επιλογής φίλτρων ===

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
            chart_type=self.chart_type_var.get(),
            region=self.region_var.get()
            # time_range δίνεται default από το constructor (2023)
        )
        if self.controller.checkData(selection):
            chart = self.controller.generateChart(selection)
            if chart:
                self.controller.display.displayChart(chart)
        else:
            self.controller.display.displayError("Δεν βρέθηκαν διαθέσιμα δεδομένα για τα επιλεγμένα φίλτρα. Παρακαλώ τροποποιήστε τις επιλογές σας.")

# === Εκκίνηση εφαρμογής ===

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