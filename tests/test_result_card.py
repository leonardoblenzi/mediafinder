import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QColor, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMenu, QToolButton, QVBoxLayout

from mediafinder.result_card import ResultCard


class ResultCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_card_shows_file_metadata_and_overflow_actions(self):
        row = {
            "file_name": "viagem-de-verao.mp4",
            "full_path": "C:/Midias/Viagens/viagem-de-verao.mp4",
            "media_type": "Vídeo",
            "classification": "Viagens",
            "directory_label": "Arquivo pessoal",
        }

        card = ResultCard(row)

        self.assertEqual(card.objectName(), "resultCard")
        self.assertIsInstance(card.layout(), QVBoxLayout)
        self.assertEqual(card.findChild(QLabel, "fileName").text(), row["file_name"])
        self.assertIn("Vídeo", card.findChild(QLabel, "badges").text())
        self.assertIn("Viagens", card.findChild(QLabel, "badges").text())
        self.assertIn("Arquivo pessoal", card.findChild(QLabel, "badges").text())
        self.assertEqual(card.findChild(QLabel, "filePath").text(), row["full_path"])

        actions_button = card.findChild(QToolButton, "actionsButton")
        self.assertIsNotNone(actions_button)
        menu = actions_button.menu()
        self.assertIsInstance(menu, QMenu)
        self.assertEqual([action.text() for action in menu.actions()], [
            "Abrir",
            "Abrir pasta",
            "Copiar caminho",
        ])

    def test_search_card_uses_icon_instead_of_loading_image_file(self):
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "poltrona.png"
            image = QImage(400, 200, QImage.Format.Format_RGB32)
            image.fill(QColor("#2563eb"))
            self.assertTrue(image.save(str(image_path)))
            row = {
                "file_name": image_path.name,
                "full_path": str(image_path),
                "media_type": "Imagem",
                "classification": "Fotos",
                "directory_label": "Catálogo",
            }

            card = ResultCard(row)

            self.assertIsNone(card._source_pixmap)
            self.assertEqual(card.preview.text(), "🖼 Imagem")
            self.assertGreaterEqual(card.minimumHeight(), 180)

    def test_menu_actions_keep_file_operation_callbacks(self):
        row = {
            "file_name": "viagem.mp4",
            "full_path": "C:/Midias/Viagens/viagem.mp4",
            "media_type": "Vídeo",
            "classification": None,
            "directory_label": "Arquivo pessoal",
        }
        card = ResultCard(row)

        with patch("mediafinder.result_card.open_file") as open_file, patch(
            "mediafinder.result_card.open_containing_folder"
        ) as open_folder:
            actions = card.findChild(QToolButton, "actionsButton").menu().actions()
            actions[0].trigger()
            actions[1].trigger()
            actions[2].trigger()

        open_file.assert_called_once_with(row["full_path"])
        open_folder.assert_called_once_with(row["full_path"])
        self.assertEqual(QApplication.clipboard().text(), row["full_path"])


if __name__ == "__main__":
    unittest.main()
