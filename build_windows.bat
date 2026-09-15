@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo [ERRO] A .venv\Scripts\python.exe nao foi encontrada.
    exit /b 1
)

for /f "tokens=1,* delims==" %%A in ('findstr /b /c:"home =" .venv\pyvenv.cfg') do set "VENV_HOME=%%B"
if not defined VENV_HOME (
    echo [ERRO] Nao foi possivel localizar o Python-base da .venv.
    exit /b 1
)

set "OLD_PATH=%PATH%"
set "PATH=%CD%\.venv\Scripts;%VENV_HOME%;%SystemRoot%\System32;%SystemRoot%;%SystemRoot%\System32\Wbem"

"%PY%" -m pip install --upgrade pip
if errorlevel 1 exit /b 1
"%PY%" -m pip install -r requirements.txt -r requirements-build.txt
if errorlevel 1 exit /b 1

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

"%PY%" -c "import PySide6; from PySide6 import QtCore, QtWidgets; print(PySide6.__version__); print(QtCore.qVersion()); print('QtWidgets OK')"
if errorlevel 1 (
    set "PATH=%OLD_PATH%"
    exit /b 1
)

"%PY%" -m PyInstaller --clean --noconfirm PesquisaMidias.spec
set "BUILD_ERROR=%ERRORLEVEL%"
set "PATH=%OLD_PATH%"
if not "%BUILD_ERROR%"=="0" exit /b %BUILD_ERROR%

"%PY%" scripts\verify_windows_bundle.py
if errorlevel 1 exit /b 1

echo BUILD OK
