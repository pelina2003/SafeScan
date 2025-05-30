import unittest
from unittest.mock import MagicMock, patch
from gui_statistics import StatisticsController, FilterSelection, DateRange, StatisticalData, Chart


class TestStatistics(unittest.TestCase):

    def setUp(self):
        # Mock του GUI display
        self.mock_display = MagicMock()
        # Mock βάση δεδομένων
        self.controller = StatisticsController(self.mock_display)
        self.controller.db_name = ":memory:"  # δεν χρησιμοποιείται εδώ λόγω mocking

    @patch("gui_statistics.sqlite3.connect")
    def test_no_data_available(self, mock_connect):
        # TC10: Δεν υπάρχουν δεδομένα
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (0,)
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        selection = FilterSelection("Πυρκαγιά", "bar", "png", "Πάτρα", DateRange("2022", "2022"))
        result = self.controller.checkData(selection)
        self.assertFalse(result)

    def test_generate_chart_no_data(self):
        # TC10 (συνέχεια): Έλεγχος ότι εμφανίζεται μήνυμα σφάλματος
        self.controller.fetchData = MagicMock(return_value=[])

        selection = FilterSelection("Πυρκαγιά", "bar", "png", "Αθήνα", DateRange("2023", "2023"))
        chart = self.controller.generateChart(selection)

        self.assertIsNone(chart)
        self.mock_display.displayError.assert_called_once()

    def test_generate_chart_bar(self):
        # TC11: Bar chart με δεδομένα
        fake_data = [
            StatisticalData("Πυρκαγιά", "Αθήνα", DateRange("2023-01", "2023-01"), 5),
            StatisticalData("Πυρκαγιά", "Αθήνα", DateRange("2023-02", "2023-02"), 8)
        ]
        self.controller.fetchData = MagicMock(return_value=fake_data)

        selection = FilterSelection("Πυρκαγιά", "bar", "png", "Αθήνα", DateRange("2023", "2023"))
        chart = self.controller.generateChart(selection)

        self.assertIsInstance(chart, Chart)
        fig = chart.render()
        self.assertIsNotNone(fig)

    def test_generate_chart_pie(self):
        # TC12: Pie chart με δεδομένα
        fake_data = [
            StatisticalData("Πλημμύρα", "Θεσσαλονίκη", DateRange("2023-01", "2023-01"), 3),
            StatisticalData("Πλημμύρα", "Θεσσαλονίκη", DateRange("2023-02", "2023-02"), 7)
        ]
        self.controller.fetchData = MagicMock(return_value=fake_data)

        selection = FilterSelection("Πλημμύρα", "pie", "png", "Θεσσαλονίκη", DateRange("2023", "2023"))
        chart = self.controller.generateChart(selection)

        self.assertIsInstance(chart, Chart)
        fig = chart.render()
        self.assertIsNotNone(fig)


if __name__ == '__main__':
    unittest.main()
