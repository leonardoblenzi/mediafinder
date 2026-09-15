from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist" / "PesquisaMidias"
ANALYSIS = ROOT / "build" / "PesquisaMidias" / "Analysis-00.toc"


def fail(message: str) -> None:
    print(f"[ERRO] {message}")
    raise SystemExit(1)


def main() -> None:
    executable = DIST / "PesquisaMidias.exe"
    if not executable.exists():
        fail(f"Executável não encontrado: {executable}")

    forbidden = []
    internal = DIST / "_internal"
    if internal.exists():
        for path in internal.rglob("*.dll"):
            name = path.name.lower()
            if name in {"icuuc.dll", "icuin.dll"} or name.startswith("icudt"):
                forbidden.append(path)
    if forbidden:
        fail("ICU externa empacotada:\n  " + "\n  ".join(map(str, forbidden)))

    if ANALYSIS.exists() and "codex-runtimes" in ANALYSIS.read_text(
        encoding="utf-8", errors="ignore"
    ).lower():
        fail("Analysis-00.toc referencia codex-runtimes.")

    print("[OK] Bundle validado.")
    print(f"[OK] Executável: {executable}")
    print(f"[OK] Python da verificação: {sys.executable}")


if __name__ == "__main__":
    main()
