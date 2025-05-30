
import unittest
from unittest.mock import MagicMock, patch
from gui_report import ReportCardApp
import tkinter as tk


class TestReportSubmit(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # δεν εμφανίζει το παράθυρο
        self.app = ReportCardApp(self.root)

    @patch("gui_report.messagebox.showerror")
    def test_submit_with_missing_fields(self, mock_showerror):
        # Κενή φωτογραφία, κενό location και σχόλια
        self.app.form.photo = None
        self.app.comment_entry.get = MagicMock(return_value="")
        self.app.location_entry.get = MagicMock(return_value="")

        self.app.submitReport()

        mock_showerror.assert_called_once_with("Σφάλμα", "Παρακαλώ συμπληρώστε όλα τα απαιτούμενα πεδία.")

    @patch("gui_report.messagebox.showinfo")
    def test_submit_with_valid_fields(self, mock_showinfo):
        self.app.form.photo = "photo.jpg"
        self.app.comment_entry.get = MagicMock(return_value="Περιγραφή")
        self.app.location_entry.get = MagicMock(return_value="Αθήνα")

        self.app.controller.createReport = MagicMock()

        self.app.submitReport()

        mock_showinfo.assert_called_once_with("Επιβεβαίωση", "Η αναφορά υποβλήθηκε επιτυχώς και βρίσκεται σε διαδικασία ελέγχου.")


if __name__ == '__main__':
    unittest.main()
