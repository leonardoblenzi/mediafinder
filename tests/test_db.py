import tempfile
import unittest
from pathlib import Path

from mediafinder.db import Database


class DatabaseSearchTests(unittest.TestCase):
    def test_default_search_caps_results_for_responsive_rendering(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database = Database(Path(temporary_directory) / "index.db")
            try:
                database.add_directory("Fotos", "C:/Midias", "Fotos")
                directory_id = database.list_directories()[0]["id"]
                rows = [
                    (
                        directory_id,
                        f"C:/Midias/poltrona-{index}.jpg",
                        f"poltrona-{index}.jpg",
                        ".jpg",
                        "Imagem",
                        "Fotos",
                        f"poltrona {index}",
                        0,
                        0,
                    )
                    for index in range(61)
                ]
                database.replace_directory_index(directory_id, rows)

                results = database.search("poltrona")

                self.assertEqual(len(results), 60)
            finally:
                database.close()
