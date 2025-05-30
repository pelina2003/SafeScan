import unittest
from unittest.mock import patch
from gui_report import CameraSystem


class TestCameraSystem(unittest.TestCase):

    @patch("gui_report.messagebox.askyesno")
    def test_permission_granted(self, mock_askyesno):
        mock_askyesno.return_value = True
        camera = CameraSystem()
        result = camera.requestPermission()
        self.assertTrue(result)

    @patch("gui_report.messagebox.askyesno")
    def test_permission_denied(self, mock_askyesno):
        mock_askyesno.return_value = False
        camera = CameraSystem()
        result = camera.requestPermission()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
