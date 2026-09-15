import os
import sqlite3
from pathlib import Path
from typing import Iterable

from .utils import normalize_text


class Database:
    def __init__(self, db_path: str | Path | None = None):
        if db_path is None:
            appdata = Path(os.getenv("APPDATA") or Path.home())
            self.data_dir = appdata / "PesquisaMidias"
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = self.data_dir / "media_index.db"
        else:
            self.db_path = Path(db_path)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_schema()

    def create_schema(self):
        self.conn.executescript(
            """
            PRAGMA journal_mode=WAL;

            CREATE TABLE IF NOT EXISTS directories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                path TEXT NOT NULL UNIQUE,
                classification TEXT,
                enabled INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS media_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                directory_id INTEGER NOT NULL,
                full_path TEXT NOT NULL UNIQUE,
                file_name TEXT NOT NULL,
                extension TEXT,
                media_type TEXT NOT NULL,
                classification TEXT,
                searchable_text TEXT NOT NULL,
                mtime REAL,
                size_bytes INTEGER,
                FOREIGN KEY(directory_id) REFERENCES directories(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_media_searchable_text
            ON media_files(searchable_text);

            CREATE INDEX IF NOT EXISTS idx_media_type
            ON media_files(media_type);

            CREATE INDEX IF NOT EXISTS idx_media_classification
            ON media_files(classification);
            """
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    def list_directories(self):
        cur = self.conn.execute(
            "SELECT * FROM directories ORDER BY label COLLATE NOCASE"
        )
        return cur.fetchall()

    def add_directory(self, label: str, path: str, classification: str | None):
        self.conn.execute(
            """
            INSERT INTO directories(label, path, classification, enabled)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(path) DO UPDATE SET
                label = excluded.label,
                classification = excluded.classification,
                enabled = 1
            """,
            (label.strip(), path.strip(), (classification or "").strip() or None),
        )
        self.conn.commit()

    def update_directory(self, directory_id: int, label: str, path: str, classification: str | None):
        self.conn.execute(
            """
            UPDATE directories
            SET label=?, path=?, classification=?
            WHERE id=?
            """,
            (label.strip(), path.strip(), (classification or "").strip() or None, directory_id),
        )
        self.conn.commit()

    def delete_directory(self, directory_id: int):
        self.conn.execute("DELETE FROM media_files WHERE directory_id=?", (directory_id,))
        self.conn.execute("DELETE FROM directories WHERE id=?", (directory_id,))
        self.conn.commit()

    def replace_directory_index(self, directory_id: int, rows: Iterable[tuple]):
        with self.conn:
            self.conn.execute(
                "DELETE FROM media_files WHERE directory_id=?",
                (directory_id,),
            )
            self.conn.executemany(
                """
                INSERT OR REPLACE INTO media_files(
                    directory_id,
                    full_path,
                    file_name,
                    extension,
                    media_type,
                    classification,
                    searchable_text,
                    mtime,
                    size_bytes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows,
            )

    def clear_all_index(self):
        self.conn.execute("DELETE FROM media_files")
        self.conn.commit()

    def count_files(self):
        row = self.conn.execute("SELECT COUNT(*) AS n FROM media_files").fetchone()
        return row["n"]

    def distinct_classifications(self):
        cur = self.conn.execute(
            """
            SELECT DISTINCT classification
            FROM media_files
            WHERE classification IS NOT NULL AND TRIM(classification) <> ''
            ORDER BY classification COLLATE NOCASE
            """
        )
        return [r["classification"] for r in cur.fetchall()]

    def search(self, query: str, media_filter: str = "Todos", classification_filter: str = "Todas", limit: int = 60):
        normalized = normalize_text(query)
        tokens = [t for t in normalized.split(" ") if t]

        where = []
        params = []

        for token in tokens:
            where.append("searchable_text LIKE ?")
            params.append(f"%{token}%")

        if media_filter != "Todos":
            where.append("media_type = ?")
            params.append(media_filter)

        if classification_filter != "Todas":
            if classification_filter == "Sem classificação":
                where.append("(classification IS NULL OR TRIM(classification) = '')")
            else:
                where.append("classification = ?")
                params.append(classification_filter)

        sql = """
            SELECT
                mf.*,
                d.label AS directory_label,
                d.path AS directory_path
            FROM media_files mf
            JOIN directories d ON d.id = mf.directory_id
        """

        if where:
            sql += " WHERE " + " AND ".join(where)

        sql += """
            ORDER BY
                CASE WHEN file_name LIKE ? THEN 0 ELSE 1 END,
                file_name COLLATE NOCASE
            LIMIT ?
        """
        params.extend([f"%{query.strip()}%", limit])

        cur = self.conn.execute(sql, params)
        return cur.fetchall()
