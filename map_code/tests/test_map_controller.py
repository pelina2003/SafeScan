import unittest
from map_controller import MapController
from unittest.mock import patch
from report import Report

class TestMapController(unittest.TestCase):

    @patch("db_manager.DBManager.get_confirmed_reports")
    def test_db_error(self, mock_get):
        mock_get.return_value = None
        controller = MapController()
        result = controller.update_map()
        self.assertEqual(result, "db_error")

    @patch("db_manager.DBManager.get_confirmed_reports")
    def test_no_reports(self, mock_get):
        mock_get.return_value = []
        controller = MapController()
        result = controller.update_map()
        self.assertEqual(result, "no_reports")

    @patch("db_manager.DBManager.get_confirmed_reports")
    def test_all_valid_reports(self, mock_get):
        mock_get.return_value = [
            Report(1, "Πυρκαγιά", 37.98, 23.72, "confirmed")
        ]
        controller = MapController()
        result = controller.update_map()
        self.assertEqual(result, "ok")

    @patch("db_manager.DBManager.get_confirmed_reports")
    def test_partial_data(self, mock_get):
        mock_get.return_value = [
            Report(1, "Πλημμύρα", None, 23.72, "confirmed"),  # invalid
            Report(2, "Ατύχημα", 40.64, 22.94, "confirmed")   # valid
        ]
        controller = MapController()
        result = controller.update_map()
        self.assertEqual(result, "partial_data")

    @patch("db_manager.DBManager.get_confirmed_reports")
    def test_all_invalid_reports(self, mock_get):
        mock_get.return_value = [
            Report(1, "Φωτιά", None, None, "confirmed"),
            Report(2, "Πλημμύρα", None, None, "confirmed")
        ]
        controller = MapController()
        result = controller.update_map()
        self.assertEqual(result, "partial_data")

