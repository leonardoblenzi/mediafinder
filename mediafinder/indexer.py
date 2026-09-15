import os
from pathlib import Path

from .utils import MEDIA_EXTENSIONS, media_type, normalize_text


def scan_directory(directory_row, progress_callback=None):
    directory_id = directory_row["id"]
    root_path = directory_row["path"]
    classification = directory_row["classification"]

    rows = []
    count = 0

    if not os.path.isdir(root_path):
        raise FileNotFoundError(f"Diretório não encontrado ou sem acesso: {root_path}")

    for root, dirs, filenames in os.walk(root_path):
        for filename in filenames:
            path = Path(root) / filename
            ext = path.suffix.lower()

            if ext not in MEDIA_EXTENSIONS:
                continue

            try:
                stat = path.stat()
            except OSError:
                continue

            # Inclui o caminho relativo para permitir busca pelo nome das pastas.
            try:
                relative = str(path.relative_to(root_path))
            except Exception:
                relative = str(path)

            searchable = normalize_text(f"{filename} {relative}")

            rows.append(
                (
                    directory_id,
                    str(path),
                    filename,
                    ext,
                    media_type(str(path)),
                    classification,
                    searchable,
                    stat.st_mtime,
                    stat.st_size,
                )
            )

            count += 1
            if progress_callback and count % 100 == 0:
                progress_callback(count, filename)

    return rows
