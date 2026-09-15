# Clean Windows Bundle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate the Windows installer using only the project's `.venv`, without DLLs injected from developer-tool paths.

**Architecture:** Pin the Qt and PyInstaller versions in project requirements. A bundle guard removes binaries discovered from external Codex runtime paths and rejects unexpected ICU DLLs. The Windows build script sanitizes `PATH`, builds through `.venv`, and validates the result before the installer is compiled.

**Tech Stack:** Python 3.10 virtual environment, PySide6 6.8.3, PyInstaller 6.18.0, Inno Setup.

---

### Task 1: Test the binary bundle guard

**Files:**
- Create: `scripts/bundle_guard.py`
- Create: `tests/test_bundle_guard.py`

- [ ] **Step 1: Write the failing test**

```python
from scripts.bundle_guard import should_exclude_binary

def test_excludes_cortex_runtime_and_icu_binaries():
    assert should_exclude_binary(('icuuc.dll', r'C:\\Users\\USER\\.cache\\codex-runtimes\\poppler\\icuuc.dll', 'BINARY'))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_bundle_guard -v`

Expected: `ModuleNotFoundError: No module named 'scripts.bundle_guard'`.

- [ ] **Step 3: Write minimal implementation**

```python
def should_exclude_binary(entry):
    destination, source, _ = entry
    return 'codex-runtimes' in source.lower() or destination.lower().endswith('icuuc.dll')
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_bundle_guard -v`

Expected: `OK`.

### Task 2: Make the Windows bundle reproducible

**Files:**
- Modify: `requirements.txt`
- Create: `requirements-build.txt`
- Create: `PesquisaMidias.spec`
- Create: `scripts/verify_windows_bundle.py`
- Create: `build_windows.bat`

- [ ] **Step 1: Pin dependencies and build from `.venv`**

Set `PySide6==6.8.3`, `PyInstaller==6.18.0`, sanitize `PATH` before the PyInstaller call, and use `.venv\\Scripts\\python.exe` for every command.

- [ ] **Step 2: Validate the frozen output**

Reject `icuuc.dll`, `icuin.dll`, `icudt*.dll`, or `codex-runtimes` references in `Analysis-00.toc`.

- [ ] **Step 3: Build and verify**

Run: `build_windows.bat`

Expected: `BUILD OK` and `dist\\PesquisaMidias\\PesquisaMidias.exe` exists.

### Task 3: Produce the installer

**Files:**
- Modify: `installer.iss`

- [ ] **Step 1: Set version 1.0.4**

Set `AppVersion` and output filename to `1.0.4`.

- [ ] **Step 2: Compile and hash**

Run Inno Setup against `installer.iss`, then calculate SHA-256 for `installer-output\\Instalar-Pesquisa-de-Midias-1.0.4.exe`.
