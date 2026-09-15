import unittest
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

from mediafinder.main_window import MainWindow


class FakeDatabase:
    def list_directories(self):
        return [{"id": 1, "label": "Fotos", "enabled": 1}]

    def distinct_classifications(self):
        return []

    def count_files(self):
        return 4


class MainWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.application = QApplication.instance() or QApplication([])

    def test_opening_window_does_not_schedule_automatic_reindex(self):
        with patch("mediafinder.main_window.QTimer.singleShot") as single_shot:
            MainWindow(FakeDatabase())

        single_shot.assert_not_called()

