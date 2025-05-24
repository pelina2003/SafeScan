import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import sqlite3
from datetime import datetime
import os

# === Entity ===
class Report:
    def __init__(self, photo=None, comments="", location=""):
        self._reportId = self._generateId()
        self._photo = photo
        self._comments = comments
        self._location = location
        self._status = "draft"
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _generateId(self):
        return f"RPT{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def submit(self):
        self._status = "submitted"

    def sendForValidation(self):
        self._status = "pending_review"

    def getData(self):
        return (self._reportId, self._photo, self._location, self._comments, self._status, self._timestamp)

# === Boundary ===
class ReportForm:
    def __init__(self):
        self.comments = ""
        self.location = ""
        self.photo = None

    def fillComments(self, comments):
        self.comments = comments

    def fillLocation(self, location):
        self.location = location

    def attachPhoto(self, photo):
        self.photo = photo

    def submitForm(self, controller):
        return controller.createReport(self.photo, self.comments, self.location)

# === System Component ===
class CameraSystem:
    def requestPermission(self):
        return messagebox.askyesno("Άδεια Πρόσβασης", "Η εφαρμογή ζητά πρόσβαση στην κάμερα. Επιτρέπετε;")

    def activate(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Σφάλμα", "Δεν είναι διαθέσιμη η κάμερα.")
            return None
        return cap

    def takePhoto(self, cap):
        messagebox.showinfo("Οδηγία", "Πατήστε SPACE για λήψη ή ESC για ακύρωση.")
        photo_taken = False
        path = None
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Λήψη Φωτογραφίας", frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
            elif key == 32:
                path = "captured_photo.jpg"
                cv2.imwrite(path, frame)
                photo_taken = True
                break
        cap.release()
        cv2.destroyAllWindows()
        return path if photo_taken else None

# === Persistence ===
class DBManager:
    def __init__(self, db_name="reports.db"):
        self._db_name = db_name
        self._expected_schema = ["id", "photo_path", "location", "comments", "status", "submission_time"]
        self.initDatabase()

    def initDatabase(self):
        reset_required = False
        if os.path.exists(self._db_name):
            try:
                conn = sqlite3.connect(self._db_name)
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(reports)")
                existing_columns = [row[1] for row in cursor.fetchall()]
                if existing_columns != self._expected_schema:
                    reset_required = True
                conn.close()
            except Exception:
                reset_required = True

        if reset_required:
            os.remove(self._db_name)

        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                photo_path TEXT,
                location TEXT,
                comments TEXT,
                status TEXT,
                submission_time TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def saveReport(self, report):
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reports (id, photo_path, location, comments, status, submission_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, report.getData())
        conn.commit()
        conn.close()

# === Control ===
class ReportController:
    def __init__(self):
        self._db = DBManager()

    def checkRequiredFields(self, photo, comments, location):
        return all([photo, comments.strip(), location.strip()])

    def createReport(self, photo, comments, location):
        report = Report(photo, comments, location)
        report.submit()
        report.sendForValidation()
        self._db.saveReport(report)
        return report

# === Entity ===
class ConfirmationMessage:
    def __init__(self, text):
        self.text = text

    def display(self):
        messagebox.showinfo("Επιβεβαίωση", self.text)

# === GUI ===
class ReportCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Αναφορά Περιστατικού")
        self.root.geometry("380x550")
        self.root.configure(bg="#f0f0f0")

        self.controller = ReportController()
        self.form = ReportForm()
        self.camera = CameraSystem()
        self.tk_image = None

        card = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=500)

        self.img_label = tk.Label(card, text="(Καμία εικόνα)", bg="white")
        self.img_label.pack(pady=(10, 5))

        loc_frame = tk.Frame(card, bg="white")
        loc_frame.pack(pady=(10, 5), fill="x", padx=20)
        tk.Label(loc_frame, text="📍 Τοποθεσία", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        self.location_entry = tk.Entry(loc_frame, font=("Arial", 10))
        self.location_entry.pack(fill="x")

        desc_frame = tk.Frame(card, bg="white")
        desc_frame.pack(pady=(10, 5), fill="x", padx=20)
        tk.Label(desc_frame, text="📝 Περιγραφή", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        self.comment_entry = tk.Text(desc_frame, height=4, font=("Arial", 10))
        self.comment_entry.pack(fill="x")

        photo_btn = tk.Button(card, text="📸 Λήψη Φωτογραφίας", command=self.takePhoto)
        photo_btn.pack(pady=10)

        submit_btn = tk.Button(card, text="Υποβολή", bg="#2962ff", fg="white",
                               font=("Arial", 11, "bold"), command=self.submitReport)
        submit_btn.pack(pady=10, ipadx=20, ipady=5)

    def takePhoto(self):
        if not self.camera.requestPermission():
            messagebox.showinfo("Άρνηση Άδειας", "Η πρόσβαση στην κάμερα απορρίφθηκε. Δεν θα ληφθεί φωτογραφία.")
            return

        cap = self.camera.activate()
        if not cap:
            return

        photo_path = self.camera.takePhoto(cap)
        if photo_path:
            self.form.attachPhoto(photo_path)
            self.displayPhoto(photo_path)

    def displayPhoto(self, path):
        try:
            image = Image.open(path)
            image = image.resize((320, 180))
            self.tk_image = ImageTk.PhotoImage(image)
            self.img_label.configure(image=self.tk_image, text="")
        except Exception:
            self.img_label.configure(text="(Αποτυχία εμφάνισης εικόνας)")

    def submitReport(self):
        comments = self.comment_entry.get("1.0", "end").strip()
        location = self.location_entry.get()

        self.form.fillComments(comments)
        self.form.fillLocation(location)

        if not self.controller.checkRequiredFields(self.form.photo, self.form.comments, self.form.location):
            messagebox.showerror("Σφάλμα", "Παρακαλώ συμπληρώστε όλα τα πεδία και προσθέστε φωτογραφία.")
            return

        self.form.submitForm(self.controller)
        msg = ConfirmationMessage("Η αναφορά σας υποβλήθηκε με επιτυχία και βρίσκεται σε διαδικασία ελέγχου.")
        msg.display()
        SuccessWindow(self.root)

# === Επιβεβαίωση ===
class SuccessWindow:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.win.title("Επιτυχία")
        self.win.geometry("300x350")
        self.win.configure(bg="white")
        self.win.resizable(False, False)

        tk.Label(self.win, text="Υποβολή Επιτεύχθηκε", font=("Arial", 14, "bold"), bg="white").pack(pady=(30, 10))

        canvas = tk.Canvas(self.win, width=100, height=100, bg="white", highlightthickness=0)
        canvas.pack()
        canvas.create_oval(10, 10, 90, 90, fill="#4CAF50", outline="")
        canvas.create_line(35, 55, 50, 70, width=5, fill="white")
        canvas.create_line(50, 70, 75, 40, width=5, fill="white")

        tk.Label(self.win, text="Η αναφορά βρίσκεται σε διαδικασία ελέγχου.", bg="white", font=("Arial", 10)).pack(pady=15)

       

# === Εκκίνηση ===
if __name__ == "__main__":
    root = tk.Tk()
    app = ReportCardApp(root)
    root.mainloop()
