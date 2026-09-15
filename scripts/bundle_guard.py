from pathlib import Path


def should_exclude_binary(entry):
    destination, source, _ = entry
    destination = str(destination).replace("/", "\\").lower()
    source = str(source).replace("/", "\\").lower()
    filename = Path(destination).name

    return (
        "codex-runtimes" in source
        or filename in {"icuuc.dll", "icuin.dll"}
        or filename.startswith("icudt")
    )
