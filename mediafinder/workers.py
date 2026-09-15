from PySide6.QtCore import QObject, Signal, Slot

from .db import Database
from .indexer import scan_directory


class IndexWorker(QObject):
    progress = Signal(str)
    error = Signal(str)
    finished = Signal(int)

    def __init__(self, db_path, directories):
        super().__init__()
        self.db_path = db_path
        self.directories = directories

    @Slot()
    def run(self):
        total = 0
        database = None
        try:
            database = Database(self.db_path)
            for d in self.directories:
                if not d["enabled"]:
                    continue

                self.progress.emit(f"Indexando: {d['label']}")

                def cb(count, filename):
                    self.progress.emit(
                        f"{d['label']}: {count} arquivos encontrados..."
                    )

                try:
                    rows = scan_directory(d, cb)
                    database.replace_directory_index(d["id"], rows)
                    total += len(rows)
                    self.progress.emit(
                        f"{d['label']}: {len(rows)} arquivos indexados."
                    )
                except Exception as exc:
                    self.error.emit(str(exc))

            self.finished.emit(total)
        except Exception as exc:
            self.error.emit(str(exc))
            self.finished.emit(total)
        finally:
            if database is not None:
                database.close()
