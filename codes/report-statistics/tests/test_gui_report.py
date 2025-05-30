import unittest
from unittest.mock import MagicMock
from gui_report import ReportController, DBManager


class TestReportCreation(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock(spec=DBManager)
        self.controller = ReportController()
        self.controller._db = self.mock_db

    def test_missing_fields(self):
        self.assertFalse(self.controller.checkRequiredFields(None, "", ""))

    def test_valid_submission(self):
        report = self.controller.createReport("photo.jpg", "Περιστατικό", "Θεσσαλονίκη")
        self.assertEqual(report._status, "pending_review")
        self.mock_db.saveReport.assert_called_once()

    def test_db_save_failure(self):
        self.mock_db.saveReport.side_effect = Exception("DB Failure")
        with self.assertRaises(Exception):
            self.controller.createReport("photo.jpg", "Περιστατικό πλημμύρας", "Καλαμάτα")

    def test_only_photo_provided(self):
        result = self.controller.checkRequiredFields("photo.jpg", "", "")
        self.assertFalse(result)

    def test_whitespace_inputs(self):
        result = self.controller.checkRequiredFields("photo.jpg", "   ", "  ")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
