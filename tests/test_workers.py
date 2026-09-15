import tempfile
import unittest
from pathlib import Path

from mediafinder.db import Database
from mediafinder.workers import IndexWorker


class IndexWorkerTests(unittest.TestCase):
    def test_worker_indexes_with_its_own_connection(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            media_directory = root / "midias"
            media_directory.mkdir()
            (media_directory / "poltrona.jpg").write_bytes(b"imagem")

            database = Database(root / "index.db")
            database.add_directory("Fotos", str(media_directory), "Fotos")
            directory = database.list_directories()[0]

            errors = []
            finished = []
            worker = IndexWorker(database.db_path, [directory])
            worker.error.connect(errors.append)
            worker.finished.connect(finished.append)
            worker.run()

            self.assertEqual(errors, [])
            self.assertEqual(finished, [1])
            self.assertEqual(database.count_files(), 1)
            database.close()
